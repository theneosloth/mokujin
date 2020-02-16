FROM python:3.7

MAINTAINER Stefan Kuznetsov (skuznetsov@posteo.net)

ADD . /mokujin

WORKDIR /mokujin

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

CMD ["pipenv", "run", "python", "./src/mokujin.py"]