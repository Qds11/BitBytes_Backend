# BitBytes_Backend

## Requirements
1. Have Docker installed
2. Have Python 3.10.7 installed (you can use pyenv to manage multiple python versions)

## Dev Set-Up
1. Clone repo
2. Set-up virtual environment with python 3.10.7
3.  ```pip install -r requirements.txt```  in cmd line
4. ```docker pull redis:latest``` in cmd line
5. ```docker run --name my-redis-container -p 6379:6379 -d redis:latest``` in cmd line
6. ```python run.py``` in cmd line to run app

### API Testing
``` <your_ip_address>:5000/<your_api_endpoint>```in testing platform

e.g. ```http://192.168.1.158:5000/api/image_classification```

## img2img dev
1. rent a gpu server, like runpod, if you do not have a gpu.
2. cd img2img and run ``` ./setup.sh ``` This is for first time installation
3. ``` flask --app app run" ``` to start the app

## img2img deployment
1. img2img container will be hosted on runpod
2. ```docker-compose build img2img && docker-compose up -D img2img```
3. It will take quite a while and the container will be 35Gb