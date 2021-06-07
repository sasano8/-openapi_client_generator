# openapi_client_generator
openapiからクライアント／サーバコードを生成します。
このツールは次のコンバータを統合したものです。

- openapi to code: [openapi-generator](https://github.com/OpenAPITools/openapi-generator)
- openapi to code: [OpenAPI Generator Online](http://api.openapi-generator.tech)
- json to jsonschema: [genson](https://github.com/wolverdude/genson/)
- jsonschema to pydantic: [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator)
- pydantic to sqlalchemy: 自作


# Requirement

- Python 3.8+

# Installation

``` shell
```

# Getting started

## 生成可能なクライアントを取得する
``` shell
python3 -m openapi_client_generator client-list
```

## クライアントを生成する

指定したopenapiの仕様書からクライアントを生成し、指定したディレクトリに出力します。
インプットにするopenapiはURL(`spec-url`)またはLOCALPATH(`spec-file`)で指定可能です。

``` shell
python3 -m openapi_client_generator client-generate --override \
     --spec-url=https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/modules/openapi-generator/src/test/resources/2_0/petstore.yaml \
     --client-type=typescript-axios \
     your_output_dir
```

``` shell
python3 -m openapi_client_generator client-generate --override \
     --spec-file=petstore.yaml \
     --client-type=typescript-axios \
     your_output_dir
```

# Setup


# 開発ガイド
CONTRIBUTING.mdを参照ください。

