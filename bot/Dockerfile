FROM python:alpine3.17
LABEL maintainer='Onyshchenko Serhii <19taurus79@gmail.com>'

ARG UID=1000
ARG GID=1000
ENV UID=${UID}
ENV GID=${GID}
ENV USER=docker_user

RUN adduser -S docker_user

WORKDIR /home/docker_user/app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m", "main_bot"]
