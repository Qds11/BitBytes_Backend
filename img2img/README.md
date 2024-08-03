The package is done by OOTDiffusion team

The run model file is in run/run_ootd.py and the old way is to python run/run_ootd.py. The goal is to convert run_ootd into services/OOTDiffusionService.py and be able to call the service in routes/OOTDiffusionRoute.py

## Todo
1. Redajust the packages imports. 
2. Add a route to receive image in the request and send images back to the users in response. 
3. Create a hashmap for the model images. For example, imageMap["model 1"] = "image path"
