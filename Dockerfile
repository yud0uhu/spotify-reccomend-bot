FROM lambci/lambda:build-python3.8
ENV LANG C.UTF-8
ENV AWS_DEFAULT_REGION ap-northeast-1

ADD .env etc/env

CMD pip install -r requirements.txt -t /var/task && \
  zip -9 deploy_package.zip function.py && \
  zip -r9 deploy_package.zip *