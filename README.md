# 仕様

## 動作確認

```
docker run --rm -v $(pwd):/var/task lambci/lambda:python3.8 function.lambda_handler
```

- win(cmd):"%cd%"
- linux/mac:$(pwd)

## ビルド

```
docker build -t aws-lambda-python3.8-spotify-reccomend-bot .
```

## デプロイファイルを作成

```
docker run --rm -v "%cd%":/var/task aws-lambda-python3.8-spotify-reccomend-bot:latest
```

## デプロイ

```
aws lambda create-function --function-name docker-lambda-python-test --zip-file fileb://deploy_package.zip --handler function.lambda_handler --runtime python3.8 --timeout 10 --memory-size 1024 --role arn:aws:iam::\***\*\*\*\*\*\*\***:role/lambda-role --profile [iam-username]
```
