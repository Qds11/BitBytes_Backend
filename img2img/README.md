The package is done by OOTDiffusion team. https://github.com/levihsu/OOTDiffusion

The package has been converted into flask restful API.

## Todo
1. Test the app

## How to use the API
1. Send a POST request to /generate endpoint
2. The request must be in multipart form-data
3. ![alt text](./images/request.png)
4. modelType. To select the AI model to detect and mask the body. hd:VITON-HD (upperbody only) and dc:Dress Code (upperbody, lowerbody and dress)
4. category. It is the type of clothing item you want to generate. 0: upperbody , 1: lowerbody, 2: dress
5. modelSelection. It is to select your model. The model are located in images/model. 1: images/model/model_1.png, 2: images/model/model_2.png
6. imageScale. The parameter allows you to scale the generated image. This can be useful if you need the output image to be of a specific size. The default value is 1.0, meaning no scaling. You can adjust this value to scale the image up or down as needed. Higher value means more computing.
7. nSteps. It determines the number of steps the model takes during the image generation process. More steps generally result in higher quality images but also increase the computation time. 
8. nSamples. It determines how many images it will generate. Best to keep it at 1 as it consumes alot of computation beyond 1.
9. seed. It initializes the random number generator for the image generation process. By setting a specific seed value, you can ensure that the generated images are reproducible. Recommended Seeds are 3661457687, 3661457785
10. The response will be an url to an image stored in S3 Bucket.

## Enviroment Variables
CHECKPOINT_PATH
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
S3_Bucket