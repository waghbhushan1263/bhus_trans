from flask import Flask, request, render_template, jsonify
from googletrans import Translator
import pdfplumber
from io import BytesIO

app = Flask(__name__, template_folder='../templates')  # Point to templates outside api/
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "No file uploaded", 400
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return "No file selected", 400
        
        # Process PDF in memory
        pdf_content = extract_text_from_pdf(pdf_file)
        return render_template('display.html', pdf_content=pdf_content)
    return render_template('upload.html')

def extract_text_from_pdf(pdf_file):
    pdf_bytes = pdf_file.read()
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

@app.route('/translate', methods=['POST'])
def translate_text():
    selected_text = request.json.get('text')
    lang = request.json.get('lang', 'mr')  # Default to Marathi
    if not selected_text:
        return jsonify({'error': 'No text provided'}), 400
    translated = translator.translate(selected_text, dest=lang).text
    return jsonify({'translated_text': translated})

# Vercel needs this for serverless
if __name__ == '__main__':
    app.run()
