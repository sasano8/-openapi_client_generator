import os
import pathlib
import json
import yaml
import pytest
from pytest import TempdirFactory
from typer.testing import CliRunner

from openapi_client_generator.cli import app
from openapi_client_generator.generator import get_response


runner = CliRunner()

SPEC_URL_N = None
SPEC_URL_Y = "https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/modules/openapi-generator/src/test/resources/2_0/petstore.yaml"
SPEC_FILE_N = None
SPEC_FILE_JSON = "pet.json"
SPEC_FILE_YAML = "pet.yaml"
SPEC_FILE_YML = "pet.yml"
OVERRIDE_Y = "--override"
OVERRIDE_N = "--no-override"


@pytest.fixture(scope="session")
def spec_dir(tmpdir_factory: TempdirFactory):
    """テスト用ファイルを一時フォルダに作成する"""
    dir = tmpdir_factory.mktemp("spec")

    spec = get_api_spec()

    with open(dir.join(SPEC_FILE_JSON), "w") as f:
        s = json.dumps(spec, ensure_ascii=False)
        f.write(s)

    with open(dir.join(SPEC_FILE_YAML), "w") as f:
        s = yaml.dump(spec)
        f.write(s)

    with open(dir.join(SPEC_FILE_YML), "w") as f:
        s = yaml.dump(spec)
        f.write(s)

    return dir


def get_api_spec():
    spec_yml = get_response(SPEC_URL_Y).decode("utf-8")
    dic = yaml.safe_load(spec_yml)
    return dic


# contents of test_image.py
def test_exists_spec_file(spec_dir):
    assert os.path.exists(spec_dir)
    assert os.path.exists(spec_dir / SPEC_FILE_JSON)
    assert os.path.exists(spec_dir / SPEC_FILE_YAML)
    assert os.path.exists(spec_dir / SPEC_FILE_YML)


def test_spec_url():
    dic = get_api_spec()
    assert dic["swagger"] == "2.0"


def test_list():
    result = runner.invoke(app, ["client-list"])
    assert result.exit_code == 0
    assert "typescript-axios" in result.stdout


@pytest.mark.parametrize(
    "override, spec_url, spec_file, expected, memo",
    [
        (OVERRIDE_Y, SPEC_URL_Y, SPEC_FILE_JSON, False, "urlとfileは同時に指定できない"),
        (OVERRIDE_Y, SPEC_URL_Y, SPEC_FILE_N, True, ""),
        (OVERRIDE_Y, SPEC_URL_N, SPEC_FILE_JSON, True, ""),
        (OVERRIDE_Y, SPEC_URL_N, SPEC_FILE_YAML, True, ""),
        (OVERRIDE_Y, SPEC_URL_N, SPEC_FILE_YML, True, ""),
    ],
)
def test_download_by_spec_url(
    spec_dir,
    tmp_path,
    *,
    type_="typescript-axios",
    override,
    spec_url,
    spec_file,
    expected,
    memo
):
    args = [
        "client-generate",
        "--client-type",
        type_,
        override,
    ]

    if spec_url:
        args.append("--spec-url")
        args.append(spec_url)

    if spec_file:
        args.append("--spec-file")
        args.append(str(spec_dir / spec_file))

    d = tmp_path / "openapi_test"
    args.append(str(d))

    result = runner.invoke(app, args)

    if not expected:
        assert result.exit_code != 0
        return

    assert result.exit_code == 0
    facts = {x.name for x in os.scandir(d)}
    expected = {
        "common.ts",
        ".openapi-generator-ignore",
        "index.ts",
        "base.ts",
        ".gitignore",
        "api.ts",
        ".npmignore",
        "git_push.sh",
        ".openapi-generator",
        "configuration.ts",
    }

    intersection = set(facts) & set(expected)
    assert len(intersection) > 2  # とりあえず、２個以上想定したファイルがあれば正しいとする
