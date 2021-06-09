# ドキュメントビルド
ドキュメントをビルドするには次のコマンドをプロジェクトルートで実行します。

```
make documantation
```

ソースディレクトリが読み込まれ、ドキュメントが自動生成されます。


```
documentation:
	@rm -rf ./docs/auto
	@poetry run sphinx-apidoc --module-first -f -o ./docs/auto ./openapi_client_generator
	@poetry run sphinx-build -b singlehtml ./docs ./docs/_build

```