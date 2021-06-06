from dataclasses import dataclass
import urllib.request
import json
import yaml
import zipfile
from io import BytesIO
import tempfile
import os
import shutil


USER_AGENET = "VM322:1 Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"


@dataclass
class OpenapiClientGenerator:
    endpoint: str
    # apiサーバは非ブラウザのリクエストを受け付けてない模様のでユーザエージェントを偽装
    user_agent: str = USER_AGENET

    def get_headers(self, **kwargs):
        return {"User-Agent": self.user_agent, **kwargs}

    def get_capability(self):
        url = self.endpoint + "/api/gen/clients"
        res = get_response(url, headers=self.get_headers())
        return json.loads(res.decode("utf-8"))

    def generate_from_url(self, openapi_url: str, client_type: str):
        data = {
            "options": {},
            "openAPIUrl": openapi_url,
        }
        return self.request_generate_client(data=data, client_type=client_type)

    def generate_from_dict(self, spec: dict, client_type: str):
        data = {"options": {}, "spec": spec}
        return self.request_generate_client(data=data, client_type=client_type)

    def request_generate_client(self, data: dict, client_type: str) -> str:
        """クライアント生成を要求し、リンクを受け取る"""
        url = self.endpoint + f"/api/gen/clients/{client_type}"
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode(),
            headers={**self.get_headers(), **{"Content-Type": "application/json"}},
            method="POST",
        )

        with urllib.request.urlopen(req) as res:
            body = res.read()

        js = body.decode("utf-8")
        return json.loads(body)["link"]


class Writer:
    @staticmethod
    def extract_zip(zip: bytes, output: str, override: bool = False):
        """ファイルを指定した出力先へ解凍する"""
        z = zipfile.ZipFile(BytesIO(zip))

        with tempfile.TemporaryDirectory() as directory:
            fname = os.path.join(directory, "downloaded")
            z.extractall(fname)
            root_dir = list(os.scandir(fname))[0]

            if override:
                shutil.rmtree(output, ignore_errors=True)

            new_path = shutil.move(root_dir.path, output)

        return new_path

    @classmethod
    def save(
        cls,
        download_link: str,
        output: str,
        override: bool = False,
        headers: dict = {"User-Agent": USER_AGENET},
    ):
        zip = get_response(download_link, headers=headers)
        path = cls.extract_zip(zip=zip, output=output, override=override)
        return path


def load_spec(openapi_path: str) -> dict:
    with open(openapi_path, "r") as f:
        _ = f.read()

    arr = openapi_path.split(".")
    extension = arr[len(arr) - 1]
    spec: dict = None

    if not len(arr) >= 2:
        raise Exception("Unkown extension")
    elif "json" in extension:
        spec = json.loads(_)
    elif "yaml" in extension:
        spec = yaml.safe_load(_)
    elif "yml" in extension:
        spec = yaml.safe_load(_)
    else:
        raise Exception()

    return spec


def get_response(url, headers: dict = {}) -> bytes:
    """データをダウンロードする"""
    req = urllib.request.Request(
        url,
        method="GET",
        headers=headers,
    )
    with urllib.request.urlopen(req) as res:
        return res.read()
