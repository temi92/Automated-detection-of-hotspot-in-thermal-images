from tensorflow/tensorflow:latest

RUN mkdir /app

WORKDIR /app
ADD . .


RUN apt-get update  && apt-get upgrade -y
RUN  apt-get install -y pkg-config
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get install libcairo2-dev libjpeg-dev libgif-dev libgirepository1.0-dev -y


RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn


CMD gunicorn app:app --bind 0.0.0.0:5000 --reload