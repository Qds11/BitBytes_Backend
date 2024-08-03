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
import argparse
parser = argparse.ArgumentParser(description='run ootd')
parser.add_argument('--gpu_id', '-g', type=int, default=0, required=False)
parser.add_argument('--model_path', type=str, default="", required=True)
parser.add_argument('--cloth_path', type=str, default="", required=True)
parser.add_argument('--model_type', type=str, default="hd", required=False)
parser.add_argument('--category', '-c', type=int, default=0, required=False)
parser.add_argument('--scale', type=float, default=2.0, required=False)
parser.add_argument('--step', type=int, default=20, required=False)
parser.add_argument('--sample', type=int, default=4, required=False)
parser.add_argument('--seed', type=int, default=-1, required=False)
args = parser.parse_args()

PATH = os.getenv('CHECKPOINT_PATH')
VIT_PATH = PATH + "/clip-vit-large-patch14"
VAE_PATH = PATH + "/ootd"
UNET_PATH = PATH + "/ootd/ootd_dc/checkpoint-36000"
MODEL_PATH = PATH + "/ootd"
# print(os.path.isdir(PATH))
# print(os.path.isdir(VIT_PATH), os.path.isdir(VAE_PATH), os.path.isdir(VIT_PATH), os.path.isdir(VIT_PATH))

if not os.path.isdir(PATH):
    print(f"Current working directory: {os.getcwd()}")
    raise FileExistsError("Checkpoints does not exist")

if not os.path.isdir(VIT_PATH):
    print(f"Current working directory: {os.getcwd()}")
    raise FileExistsError("VIT_PATH does not exist")
if not os.path.isdir(VAE_PATH):
    print(f"Current working directory: {os.getcwd()}")
    raise FileExistsError("VAE_PATH does not exist")
if not os.path.isdir(VIT_PATH):
    print(f"Current working directory: {os.getcwd()}")
    raise FileExistsError("UNET_PATH does not exist")
if not os.path.isdir(VIT_PATH):
    print(f"Current working directory: {os.getcwd()}")
    raise FileExistsError("MODEL_PATH does not exist")

openpose_model = OpenPose(args.gpu_id)
parsing_model = Parsing(args.gpu_id)


category_dict = ['upperbody', 'lowerbody', 'dress']
category_dict_utils = ['upper_body', 'lower_body', 'dresses']

model_type = args.model_type # "hd" or "dc"
category = args.category # 0:upperbody; 1:lowerbody; 2:dress
cloth_path = args.cloth_path
model_path = args.model_path

image_scale = args.scale
n_steps = args.step
n_samples = args.sample
seed = args.seed

if model_type == "hd":
    model = OOTDiffusionHD(args.gpu_id, PATH)
elif model_type == "dc":
    model = OOTDiffusionDC(args.gpu_id, PATH)
else:
    raise ValueError("model_type must be \'hd\' or \'dc\'!")


if __name__ == '__main__':

    if model_type == 'hd' and category != 0:
        raise ValueError("model_type \'hd\' requires category == 0 (upperbody)!")

    cloth_img = Image.open(cloth_path).resize((768, 1024))
    model_img = Image.open(model_path).resize((768, 1024))
    keypoints = openpose_model(model_img.resize((384, 512)))
    model_parse, _ = parsing_model(model_img.resize((384, 512)))

    mask, mask_gray = get_mask_location(model_type, category_dict_utils[category], model_parse, keypoints)
    mask = mask.resize((768, 1024), Image.NEAREST)
    mask_gray = mask_gray.resize((768, 1024), Image.NEAREST)
    
    masked_vton_img = Image.composite(mask_gray, model_img, mask)
    masked_vton_img.save('./images_output/mask.jpg')

    images = model(
        model_type=model_type,
        category=category_dict[category],
        image_garm=cloth_img,
        image_vton=masked_vton_img,
        mask=mask,
        image_ori=model_img,
        num_samples=n_samples,
        num_steps=n_steps,
        image_scale=image_scale,
        seed=seed,
    )

    image_idx = 0
    for image in images:
        image.save('./images_output/out_' + model_type + '_' + str(image_idx) + '.png')
        image_idx += 1
