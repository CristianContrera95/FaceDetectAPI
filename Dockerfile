FROM python:3.8
MAINTAINER CRISTIAN_CONTRERA <cristiancontrera95@gmail.com>

RUN apt-get update
RUN apt-get install make automake cmake gcc g++ python3-dev -y
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Uncomment for production
COPY src/ .

EXPOSE 5000

RUN apt-get install ffmpeg libsm6 libxext6 -y

CMD ["python" , "run.py"]
