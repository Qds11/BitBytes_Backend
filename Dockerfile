FROM python:3.10-slim-buster

WORKDIR /bitbytes_backend

COPY . /bitbytes_backend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000


CMD ["python", "run.py"]