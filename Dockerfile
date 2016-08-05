FROM python:2.7.12
ADD . /flongo
WORKDIR /flongo
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
