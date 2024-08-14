# BitBytes_Backend

## Requirements
1. Have Docker installed

## Dev Set-Up [Music Generation Service]
1. Set-up virtual environment with python 3.10.7
2.  ```pip install --no-cache-dir -r requirements.txt``  in cmd line
3. ```docker pull redis:latest``` in cmd line
4. ```docker run --name my-redis-container -p 6379:6379 -d redis:latest``` in cmd line
5. ```python run.py``` in cmd line to run app

## Run Service [Music Generation Service]
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

