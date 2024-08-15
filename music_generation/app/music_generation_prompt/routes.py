from flask import request, jsonify
from . import music_generation_prompt_bp
from ..limiter import limiter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

@music_generation_prompt_bp.route('/', methods=['POST'])
@limiter.limit("2/minute")
def generate_prompt():
    try:
        data = request.json
        clothing_attributes = data.get('clothing_attributes')
        completion = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:personal::9rfLZpOg",
            messages=[
                {"role": "system", "content": "Based on the clothing attributes provided below, generate a concise music prompt suitable for creating advertisement music. The music should reflect the vibe of the clothing described. Detail the genre, tempo, and beat that would best match these clothing characteristics: - Season: {season} - Style: {style} - Gender: {gender} - Category: {category} - Color: {color} e.g. Category: Dress, Gender: Women, Season: Summer  ,Color: Blue  ,Style: Casual. Please structure your response as follows: - Genre: - Tempo: - Beat:"},
                {"role": "user", "content": clothing_attributes}
            ]
        )

        music_prompt = completion.choices[0].message.content

        return jsonify({'result': music_prompt})
    except Exception as e:
        print(f"Error generating music prompt: {str(e)}")
        return jsonify({'error': str(e)}), 500


