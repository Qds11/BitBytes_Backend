from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from PIL import Image

from utils.utils_ootd import get_mask_location
from utils.preprocess.openpose.run_openpose import OpenPose
from utils.preprocess.humanparsing.run_parsing import Parsing
from utils.ootd.inference_ootd_hd import OOTDiffusionHD
from utils.ootd.inference_ootd_dc import OOTDiffusionDC
import os

from dotenv import load_dotenv
load_dotenv()

modelMap = {
    1: "images/model/model_1.png",
    2: "images/model/model_2.png",
    3: "images/model/model_3.png",
    4: "images/model/model_4.png",
    5: "images/model/model_5.png",
    6: "images/model/model_6.png",
    7: "images/model/model_7.png",
    8: "images/model/model_8.png",
    9: "images/model/model_9.png",
}
category_dict = ['upperbody', 'lowerbody', 'dress']
category_dict_utils = ['upper_body', 'lower_body', 'dresses']

# modelType = "hd" or "dc"
# category = 0:upperbody; 1:lowerbody; 2:dress
def generateImage(gpuId = 1,modelType = "hd", category = "upperbody" , clothImage=None, modelSelection=None, imageScale=2.0, nSteps=20, nSamples=4, seed=1):
    print(gpuId,modelType,category, clothImage, modelSelection, imageScale, nSteps, nSamples, seed)
    PATH = os.getenv('CHECKPOINT_PATH')
    checkPath(PATH)

    openpose_model = OpenPose(gpuId)
    parsing_model = Parsing(gpuId)

    model = modelSelection(modelType, gpuId, PATH)

    clothImg = Image.open(clothImage).resize((768, 1024))
    modelImg = Image.open(modelSelection).resize((768, 1024))
    keypoints = openpose_model(modelImg.resize((384, 512)))
    model_parse, _ = parsing_model(modelImg.resize((384, 512)))

    mask, mask_gray = get_mask_location(modelType, category_dict_utils[category], model_parse, keypoints)
    mask = mask.resize((768, 1024), Image.NEAREST)
    mask_gray = mask_gray.resize((768, 1024), Image.NEAREST)
    
    masked_vton_img = Image.composite(mask_gray, modelImg, mask)
    # masked_vton_img.save('./images/images_output/mask.jpg')

    images = model(
        model_type=modelType,
        category=category_dict[category],
        image_garm=clothImg,
        image_vton=masked_vton_img,
        mask=mask,
        image_ori=modelImg,
        num_samples= nSamples,
        num_steps= nSteps,
        image_scale= imageScale,
        seed=seed,
    )

    return images

def validateAndCreatePath(path: str):
    if not os.path.isdir(path):
        print(f"Current working directory: {os.getcwd()}")
        raise FileExistsError("Checkpoints does not exist")

def checkPath(PATH: str):
    VIT_PATH = PATH + "/clip-vit-large-patch14"
    VAE_PATH = PATH + "/ootd"
    UNET_PATH = PATH + "/ootd/ootd_dc/checkpoint-36000"
    MODEL_PATH = PATH + "/ootd"
    pathList = [PATH, VIT_PATH, VAE_PATH, UNET_PATH, MODEL_PATH]
    for path in pathList:
        validateAndCreatePath(path)

def modelSelection(modelType, gpuId, PATH):
    model = None
    if modelType == "hd":
        model = OOTDiffusionHD(gpuId, PATH)
    elif modelType == "dc":
        model = OOTDiffusionDC(gpuId, PATH)
    else:
        raise ValueError("model_type must be \'hd\' or \'dc\'!")
    return model