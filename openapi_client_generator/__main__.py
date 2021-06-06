import typer
import logging

from .generator import OpenapiClientGenerator

app = typer.Typer()

logger = logging.getLogger(__name__)


@app.command()
def client_list(
    endpoint: str = "http://api.openapi-generator.tech",
):
    "Openapiから生成可能なクライアントの識別子を列挙します"
    obj = OpenapiClientGenerator(endpoint=endpoint)
    result = obj.get_capability()
    typer.echo(result)


@app.command()
def client_generate(
    output: str,
    *,
    endpoint: str = "http://api.openapi-generator.tech",
    client_type: str = "typescript-axios",
    spec_url: str = None,
    spec_file: str = None,
    override: bool = False,
):
    """指定したOpenApiSpecからクライアントを生成します"""
    assert not (spec_url and spec_file), "must be spec_url or spec_file."

    obj = OpenapiClientGenerator(endpoint=endpoint)
    if spec_url:
        path = obj.generate_from_url(
            openapi_url=spec_url,
            client_type=client_type,
            output=output,
            override=override,
        )
    elif spec_file:
        path = obj.generate_from_file(
            openapi_path=spec_file,
            client_type=client_type,
            output=output,
            override=override,
        )
    else:
        raise Exception()

    typer.echo(path)


@app.command()
def server_generate(
    output: str,
    *,
    endpoint: str = "http://api.openapi-generator.tech",
    client_type: str = "typescript-axios",
    spec_url: str = None,
    spec_file: str = None,
    override: bool = False,
):
    """指定したOpenApiSpecからサーバ用ソースコードの雛形を生成します（未実装）"""
    raise NotImplementedError()


if __name__ == "__main__":
    app()
