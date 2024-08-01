from flask import request, send_file, jsonify
import io
import torch
import torchaudio
from audiocraft.models import MusicGen
import redis
from . import music_generation_bp
import os
import uuid
from ..redis_client import redis_client

def load_model():
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    return model

def generate_music_tensors(description, duration: int):
    model = load_model()
    model.set_generation_params(
        use_sampling=True,
        top_k=250,
        duration=duration
    )
    output = model.generate(
        descriptions=[description],
        progress=True,
        return_tokens=True
    )
    return output[0]

def save_audio_to_redis(samples: torch.Tensor, key_prefix: str):
    sample_rate = 32000
    assert samples.dim() == 2 or samples.dim() == 3
    samples = samples.detach().cpu()
    if samples.dim() == 2:
        samples = samples[None, ...]
    audio_path = io.BytesIO()
    torchaudio.save(audio_path, samples[0], sample_rate, format='wav')
    audio_path.seek(0)
    redis_client.setex(f"{key_prefix}_audio", 300, audio_path.read())  # Expires in 10 mins

def fetch_audio_from_storage(key_prefix: str):
    audio_file_path = redis_client.get(f"{key_prefix}_audio_0_path")
    if not audio_file_path:
        print("no audio file")
        return None
    with open(audio_file_path, 'rb') as audio_file:
        print("has audio file")
        return audio_file.read()

@music_generation_bp.route('/', methods=['POST'])
def generate_music():
    data = request.json

    description = data.get('description')
    duration = data.get('duration', 8)  # Default to 8 seconds if not provided
    print("Description:", description)
    print("Duration:", duration)

    if not description:
        return jsonify({'error': 'Description is required'}), 400
    # Generate unique key for the user
    user_id = str(uuid.uuid4())  # or use a user ID from your authentication system
    audio_key_prefix = f"generated_music_{user_id}_{description}"

    # Generate music tensors
    music_tensors = generate_music_tensors(description, duration)
    print("Music Tensors: ", music_tensors)
    save_audio_to_redis(music_tensors, audio_key_prefix)
    print("saved audio")

    # Fetch audio from Redis
    audio_data = redis_client.get(f"{audio_key_prefix}_audio")
    # Create an in-memory binary stream and return it
    audio_stream = io.BytesIO(audio_data)
    return send_file(audio_stream, mimetype='audio/wav', as_attachment=True, download_name ='generated_music.wav')