import json

from ..apimock import APIRouter
from ..generator import OpenapiClientGenerator

router = APIRouter()


@router.get("/client/list")
def client_list(
    endpoint: str = "http://api.openapi-generator.tech",
):
    "Openapiから生成可能なクライアントの識別子を列挙します"
    obj = OpenapiClientGenerator(endpoint=endpoint)
    return obj.get_capability()


@router.post("/client/generate")
def client_generate(
    endpoint: str = "http://api.openapi-generator.tech",
    client_type: str = "typescript-axios",
    spec_url: str = None,
    spec_json: str = None,
):
    """指定したOpenApiSpecからクライアントを生成し、ダウンロードリンクを取得します"""
    assert not (spec_url and spec_json), "must be spec_url or spec_file."

    obj = OpenapiClientGenerator(endpoint=endpoint)
    if spec_url:
        download_link = obj.generate_from_url(
            openapi_url=spec_url,
            client_type=client_type,
        )
    elif spec_json:
        download_link = obj.generate_from_dict(
            spec=json.loads(spec_json),
            client_type=client_type,
        )
    else:
        raise Exception()

    return download_link
