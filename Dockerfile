from tensorflow/tensorflow:latest

RUN mkdir /app

WORKDIR /app
ADD . .

RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip install -r requirements.txt
RUN pip install gunicorn


CMD gunicorn app:app --bind 0.0.0.0:5000 --reload
