FROM python:3.7
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install tor -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt  && rm requirements.txt
RUN pip install --user --upgrade git+https://github.com/himanshudabas/twint.git@origin/twint-fixes#egg=twint

COPY ./src /app

WORKDIR /app