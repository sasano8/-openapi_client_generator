import json
import tempfile
import hjson
from fastapi.responses import PlainTextResponse
from genson import SchemaBuilder
from typing import List, Literal
from datamodel_code_generator import generate, InputFileType
from pydantic import BaseModel

from ..apimock import APIRouter


router = APIRouter()


@router.post("/to_jsonschema")
def to_jsonschema(
    all_required: bool = True,
    extension: Literal["json"] = "json",
    root_name: str = "Model",
    payload: str = '{name: "test", age: 20}',
):
    """データから型を類推したjsonschemaを生成します"""
    pyobj = hjson.loads(payload)
    assert isinstance(pyobj, dict)

    if pyobj.get("$schema"):
        raise Exception("Json schemaっぽいよ。")

    builder = SchemaBuilder()
    builder.add_schema({"type": "object", "title": root_name})
    builder.add_object(pyobj)
    return builder.to_schema()


@router.post("/to_pydantic", response_class=PlainTextResponse)
def to_pydantic(
    type_: Literal["openapi", "jsonschema", "json"] = "json",
    all_required: bool = True,
    extension: Literal["json"] = "json",
    payload: str = '{name: "test", age: 20}',
):
    """"""
    if type_ == InputFileType.Json.value:
        input_data = to_jsonschema(
            all_required=all_required, payload=payload, extension=extension
        )
        input_file_type = InputFileType.JsonSchema

    elif type_ == InputFileType.JsonSchema.value:
        input_data = hjson.loads(payload)
        input_file_type = InputFileType.JsonSchema

    elif type_ == InputFileType.OpenAPI.value:
        input_data = hjson.loads(payload)
        input_file_type = InputFileType.OpenAPI
    else:
        raise Exception()

    with tempfile.TemporaryDirectory() as dname:
        from pathlib import Path

        input_path = Path(dname) / "spec"
        output_path = Path(dname) / "tmp.py"

        with open(input_path, "w") as f:
            input = json.dumps(input_data, ensure_ascii=False)
            f.write(input)

        # 戻り値を持たないので、ファイルでやり取りする
        generate(
            input_path,
            input_file_type=input_file_type,
            force_optional_for_required_fields=not all_required,
            output=output_path,
        )

        with open(output_path, "r") as f:
            code = f.read()

    return code


@router.post("/to_sqlalchemy", response_class=PlainTextResponse)
def to_sqlalchemy(
    type_: Literal["openapi", "jsonschema", "json"] = "json",
    all_required: bool = True,
    extension: Literal["json"] = "json",
    payload: str = '{name: "test", age: 20}',
):
    code = to_pydantic(
        type_=type_, all_required=all_required, extension=extension, payload=payload
    )
    code = SqlalchemyCodeGenerator.generate_by_models(get_models_by_code(code))
    return code


def get_models_by_code(code):
    import types

    mod = types.ModuleType("tmp")
    exec(code, mod.__dict__)
    from pydantic import BaseModel
    from enum import Enum

    it_1 = (
        x
        for x in mod.__dict__.values()
        if isinstance(x, type) and not (x is BaseModel or x is Enum)
    )
    it_2 = (x for x in it_1 if issubclass(x, BaseModel) or issubclass(x, Enum))
    return list(it_2)


def to_pydantic_models(
    type_: Literal["openapi", "jsonschema", "json"] = "json",
    all_required: bool = True,
    payload: str = '{name: "test", age: 20}',
):
    code = to_pydantic(type_=type_, all_required=all_required, payload=payload)
    models = get_models_by_code(code)


class SqlalchemyCodeGenerator:
    def __init__(self, obj: BaseModel):
        self.obj = obj

    @classmethod
    def generate_by_models(cls, models: List[BaseModel]):
        codes = []
        for model in models:
            gen = SqlalchemyCodeGenerator(model)
            code = gen.output_sqlalchemy_code()
            codes.append(code)

        return "\n".join(codes)

    def output_sqlalchemy_code(self):
        fields = self.obj.__fields__.copy()

        str_indent = "  "
        decreative_base = "Base"

        lines = []
        lines.append(f"class {self.obj.__name__}Table({decreative_base}):")

        if key := fields.pop("id", None):
            lines.append(
                str_indent + "id = Column(Integer, primary_key=True, index=True)"
            )

        for field in fields.values():
            code = self.output_sqlalchemy_field(field)
            lines.append(str_indent + code)

        return "\n".join(lines)

    @classmethod
    def output_sqlalchemy_field(cls, field):
        sql_alchemy_type = cls.map_sqlalcemy_type(field.type_)
        if field.type_ is str:
            return f'{field.name} = Column({sql_alchemy_type}, blank=True, nullable=False, server_default="")'
        elif field.type_ is int:
            return f"{field.name} = Column({sql_alchemy_type}, nullable=False, server_default=0)"
        elif field.type_ is float:
            return f"{field.name} = Column({sql_alchemy_type}, nullable=False, server_default=0)"
        elif field.type_ is bool:
            return f"{field.name} = Column({sql_alchemy_type}, nullable=False, server_default=False)"
        else:
            return "Undefine"

    @classmethod
    def map_sqlalcemy_type(cls, _type):
        if _type is str:
            return "String(1023)"
        elif _type is int:
            return "Ingeger"
        elif _type is float:
            return "Float"
        elif _type is bool:
            return "Bool"
        else:
            return "Undefine"
