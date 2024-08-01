# BitBytes_Backend

## Requirements
1. Have Docker installed

## Dev Set-Up [Music Generation Service]
1. Set-up virtual environment with python 3.10.7
2.  ```pip install -r requirements.txt```  in cmd line
3. ```docker pull redis:latest``` in cmd line
4. ```docker run --name my-redis-container -p 6379:6379 -d redis:latest``` in cmd line
5. ```python run.py``` in cmd line to run app

    ### API Testing
    ``` <your_ip_address>:5100/<your_api_endpoint>```in testing platform

    e.g. ```http://192.168.1.158:5100/api/image_classification```
