# BitBytes_Backend

### Requirements
1. Have Docker installed
## Music Generation Service
### Dev Set-Up
1. Set-up virtual environment with python 3.10.7
2.  ```pip install --no-cache-dir -r requirements.txt```  in cmd line
3. ```docker pull redis:latest``` in cmd line
4. ```docker run --name my-redis-container -p 6379:6379 -d redis:latest``` in cmd line
5. ```python run.py``` in cmd line to run app

### Run Service
1. Download yml file
2. Create .env file with the following variables
    ```
    OPENAI_API_KEY= <your_openai_api_key>
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_DB=0
    ```
3. Edit env file path in yml file if your differs
4. ```docker compose up``` in cmd line
### Demo
Click on image to view demo
[![Music Generation Service Demo](https://img.youtube.com/vi/ZrmfwJmS-Tw/0.jpg)](https://www.youtube.com/watch?v=ZrmfwJmS-Tw)


## img-2-img Service

### Dev Set-Up
1. rent a gpu server, like runpod, if you do not have a gpu.
2. cd img2img and run ``` ./setup.sh ``` This is for first time installation
3. ``` flask --app app run" ``` to start the app

### Deployment Set-Up 
1. img2img container will be hosted on runpod
2. ```docker-compose build img2img && docker-compose up -D img2img```
3. It will take quite a while and the container will be 35Gb
4. TODO: Upload the dockerfile container onto runpod or vastai as the service uses GPU extensively
