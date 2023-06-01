from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests, json

app = Flask(__name__)

def detect_language(text):
    # Usa la función existente para detectar el idioma
    cog_key = os.getenv('COG_SERVICE_KEY')
    cog_region = os.getenv('COG_SERVICE_REGION')
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

    path = '/detect'
    url = translator_endpoint + path

    params = {
        'api-version': '3.0'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    language = response[0]["language"]
    return language


def get_translated_text(text, target_language):
    # Usa el código existente para obtener la traducción del texto
    cog_key = os.getenv('COG_SERVICE_KEY')
    cog_region = os.getenv('COG_SERVICE_REGION')
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

    def translate_text(text, source_language, target_language):
        # Usa la función existente para traducir el texto
        path = '/translate'
        url = translator_endpoint + path

        params = {
            'api-version': '3.0',
            'from': source_language,
            'to': [target_language]
        }

        headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-type': 'application/json'
        }

        body = [{
            'text': text
        }]

        request = requests.post(url, params=params, headers=headers, json=body)
        response = request.json()

        translation = response[0]["translations"][0]["text"]
        return translation

    # Detectar el idioma del texto de entrada
    source_language = detect_language(text)

    # Traducir si no es el mismo idioma de destino
    if source_language != target_language:
        translated_text = translate_text(text, source_language, target_language)
    else:
        translated_text = text

    return translated_text

@app.route('/', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['language']
        source_language = detect_language(text)
        translated_text = get_translated_text(text, target_language)
        return render_template('home.html', translated_text=translated_text, lang_detected=source_language)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    load_dotenv()
    app.run()
