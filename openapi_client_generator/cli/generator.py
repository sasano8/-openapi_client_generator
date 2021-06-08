import json

import typer

from ..api import generator
from ..generator import Writer, load_spec

app = typer.Typer()


@app.command()
def client_list(
    endpoint: str = "http://api.openapi-generator.tech",
):
    "Openapiから生成可能なクライアントの識別子を列挙します"
    result = generator.client_list(endpoint=endpoint)
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

    spec_json = None
    if spec_file:
        spec_dict = load_spec(spec_file)
        spec_json = json.dumps(spec_dict, ensure_ascii=False)

    download_link = generator.client_generate(
        endpoint=endpoint,
        client_type=client_type,
        spec_url=spec_url,
        spec_json=spec_json,
    )
    path = Writer.save(download_link=download_link, output=output, override=override)
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
