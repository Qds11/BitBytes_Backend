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
### Testing
1. Switch to branch music_generation_service_image
2. Create .env file with the following variables
    ```
    OPENAI_API_KEY= <your_openai_api_key>
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_DB=0
    ```
3. Edit env file path in yml file if your differs
4. ```docker compose up``` in cmd line
5. Call image_classfication api with clothing image as input
    ```
    localhost:5100/api/image_classification
    ```
    ![image](https://github.com/user-attachments/assets/fcd170f1-6081-418a-afa7-1b26b417fd4a)

6. Use image_classification api output as input for music_generation_prompt
   ```
   localhost:5100/api/music_generation_prompt
   ```
   ![image](https://github.com/user-attachments/assets/770b44eb-dd7d-459e-9a89-a3e01f83d056)
7. Use music_generation_prompt output as inout for music_generation api. It will take a while for the music to be generated.
   ```
    localhost:5100/api/music_generation
   ```
   ![image](https://github.com/user-attachments/assets/323bdb04-0712-4f6f-99bd-d068fa9299f2)

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
