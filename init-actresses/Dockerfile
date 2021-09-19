FROM public.ecr.aws/lambda/python:3.7

COPY app.py requirements.txt ./
COPY model ./model

# module内で.py 以外のファイルへのパスは参照できないためmoduleから分離させる
COPY inputs /opt/ml/inputs

RUN python3.7 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
