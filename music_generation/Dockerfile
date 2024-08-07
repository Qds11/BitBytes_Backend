FROM python:3.10-slim-buster

# RUN apt-get install -y libgl1-mesa-dev

WORKDIR /bitbytes_backend/music_generation

COPY . /bitbytes_backend/music_generation/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5100


CMD ["python", "run.py"]