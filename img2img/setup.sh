#!/bin/sh

pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip install -r requirements.txt --no-cache-dir
cd utils/checkpoints
git lfs install
git clone https://huggingface.co/levihsu/OOTDiffusion
mv -f OOTDiffusion/checkpoints/* . 
rm -rf OOTDiffusion/
git clone https://huggingface.co/openai/clip-vit-large-patch14
wait