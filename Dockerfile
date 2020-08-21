FROM python:3.8-alpine
MAINTAINER CRISTIAN_CONTRERA <cristiancontrera95@gmail.com>

RUN apk update
RUN apk add make automake cmake gcc g++ python3-dev
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Uncomment for production
COPY src/ .

EXPOSE 5000

CMD ["python", "run.py"]
