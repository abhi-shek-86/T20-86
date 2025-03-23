import os
from flask import Flask, render_template, request, jsonify
from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)

# Updated supported language pairs
SUPPORTED_PAIRS = {
    ("en", "fr"), ("en", "hi"), ("en", "es"),  # English to French, Hindi, Spanish
    ("hi", "en"),  # Hindi to English
    ("hi", "te"), ("te", "hi"),  # Hindi to Telugu, Telugu to Hindi
    ("fr", "de"), ("de", "fr")   # French to German, German to French
}

# Function to get available target languages based on selection
def get_available_targets():
    supported_dict = {}
    for src, tgt in SUPPORTED_PAIRS:
        if src not in supported_dict:
            supported_dict[src] = []
        supported_dict[src].append(tgt)
    return supported_dict

# Function to translate text
def translate_text(text, src_lang, tgt_lang):
    if (src_lang, tgt_lang) not in SUPPORTED_PAIRS:
        return f"❌ Error: Translation from '{src_lang}' to '{tgt_lang}' is not supported."
    
    try:
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        return translated_text
    except Exception as e:
        return f"⚠ Error: {e}. Ensure the selected language pair is correct."

@app.route('/')
def index():
    return render_template('index.html', supported_pairs=get_available_targets())

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get("text")
    src_lang = data.get("src_lang")
    tgt_lang = data.get("tgt_lang")

    translation = translate_text(text, src_lang, tgt_lang)
    return jsonify({"translation": translation})

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
11