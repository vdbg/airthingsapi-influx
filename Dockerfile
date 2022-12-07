FROM python:3.9-alpine

RUN addgroup -S airthings && adduser -S airthings -G airthings

USER airthings

WORKDIR /app

# Prevents Python from generating pyc files to reduce image size
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
# Install location of upgraded pip
ENV PATH /home/airthings/.local/bin:$PATH

COPY requirements.txt     /app/

RUN pip install --no-cache-dir --disable-pip-version-check --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY *.py                 /app/
COPY template.config.yaml /app/

ENTRYPOINT python main.py
