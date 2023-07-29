FROM python:3.11-slim-buster AS system
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONPYCACHEPREFIX=/.pycache
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl gettext libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
    rm -rf /var/lib/apt/lists/*

ARG USER_ID=1000
RUN useradd --create-home --user-group -u $USER_ID user

USER $USER_ID
WORKDIR /home/user


RUN curl -sSL https://install.python-poetry.org | python3 -

# Create a virtual env in home directory.
ENV VIRTUAL_ENV=/home/user/.venv
ENV PATH="${VIRTUAL_ENV}/bin:/home/user/.local/bin:${PATH}"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /home/user
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./piccolo_conf.py .

RUN poetry install

COPY --chown=user ./repetitor_backend ./repetitor_backend
COPY --chown=user ./dbfilling ./dbfilling
# COPY --chown=user ./repetitor-389219-07b881b77aa7.json ./repetitor-389219-07b881b77aa7.json

CMD ["python3", "-m", "uvicorn", "repetitor_backend.app:app", "--host", "0.0.0.0", "--port", "80"]