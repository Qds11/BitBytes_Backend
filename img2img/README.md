The package is done by OOTDiffusion team. https://github.com/levihsu/OOTDiffusion

The run model file is in run/run_ootd.py and the old way is to python run/run_ootd.py. The goal is to convert run_ootd into services/OOTDiffusionService.py and be able to call the service in routes/OOTDiffusionRoute.py

## Todo
1. Find a way to store the images and send them back to client. Current thinking of using s3 and send urls back to client. See TODO routes/OOTDiffusionRoute.py 
2. Test it
3. Handle the errors better in route or service
