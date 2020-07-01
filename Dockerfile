from tensorflow/tensorflow:latest

RUN mkdir /app

WORKDIR /app
ADD . .


RUN apt-get update  && apt-get upgrade -y
RUN  apt-get install -y pkg-config
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get install libcairo2-dev libjpeg-dev libgif-dev libgirepository1.0-dev -y

RUN apt-get install python2.7 python-pip -y 

RUN python2.7 -m pip install --upgrade pip
RUN python2.7 -m pip install -r requirements.txt
RUN python2.7 -m pip install gunicorn


#CMD gunicorn app:app --bind 0.0.0.0:5000 --reload

CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload

