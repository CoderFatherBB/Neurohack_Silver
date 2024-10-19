import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import spacy
from textblob import TextBlob
import fitz  # PyMuPDF
from docx import Document
import pandas as pd
import json
import xml.etree.ElementTree as ET
from lxml import etree
import html

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xlsx', 'json', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

nlp = spacy.load("en_core_web_sm")
model_name = 'google/flan-t5-small'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

def clean_text(text):
    text = html.unescape(text)
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    return text

def analyze_content_structure(text):
    doc = nlp(text)
    num_entities = len(doc.ents)
    num_sentences = len(list(doc.sents))
    num_tokens = len(doc)
    num_keywords = sum(1 for token in doc if not token.is_stop)
    num_bullets = text.count('- ') + text.count('* ') + text.count('• ')
    num_arrows = text.count('->') + text.count('=>')

    if num_bullets > 3 or 'list' in text.lower():
        return "bullet points"
    elif num_arrows > 2 or "process" in text.lower() or "steps" in text.lower():
        return "flowchart"
    elif num_entities > 5 and num_keywords / num_tokens < 0.5:
        return "table"
    else:
        return "paragraph"

def clean_summary(summary, style):
    if style == "bullet points":
        cleaned_lines = []
        for line in summary.split(". "):
            line = line.strip().lstrip("1234567890.- ")
            if line:
                cleaned_lines.append(f"- {line}")
        return "\n".join(cleaned_lines)
    elif style == "flowchart":
        cleaned_lines = []
        for line in summary.split(". "):
            line = line.strip().lstrip("1234567890.- ")
            if line:
                cleaned_lines.append(f"-> {line}")
        return "\n".join(cleaned_lines)
    else:
        return summary.replace(". ", ".\n")

def summarize_text(text, context=''):
    text = clean_text(text)
    style = analyze_content_structure(text)
    combined_input = context + "\n" + text if context else text
    prompt = f"summarize the content as {style}: {combined_input}"

    input_tokens = tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
    input_length = input_tokens.shape[1]
    max_length = 5000
    min_length = 100

    summary_ids = model.generate(
        input_tokens,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    cleaned_summary = clean_summary(summary, style)
    return cleaned_summary

def process_image_with_ocr(file_path):
    try:
        image = Image.open(file_path)
        custom_oem_psm_config = "/Users/adityachavan/Downloads/TEXTSUMM/eng.traineddata"
        extracted_text = pytesseract.image_to_string(image, config=custom_oem_psm_config)
        return extracted_text.strip()
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")

def process_pdf(file_path):
    try:
        pdf_document = fitz.open(file_path)
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF processing failed: {str(e)}")

def process_docx(file_path):
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return "\n".join(text).strip()
    except Exception as e:
        raise Exception(f"DOCX processing failed: {str(e)}")

def process_xlsx(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=None)
        text = []
        for sheet_name, sheet_data in df.items():
            text.append(f"Sheet: {sheet_name}\n")
            text.append(sheet_data.to_string(index=False))
        return "\n\n".join(text).strip()
    except Exception as e:
        raise Exception(f"XLSX processing failed: {str(e)}")

def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    def extract_text_from_json(data, text=""):
        if isinstance(data, dict):
            for value in data.values():
                text = extract_text_from_json(value, text)
        elif isinstance(data, list):
            for item in data:
                text = extract_text_from_json(item, text)
        elif isinstance(data, str):
            text += data + " "
        return text
    
    extracted_text = extract_text_from_json(data)
    return extracted_text

def process_xml(file_path):
    with open(file_path, 'r') as file:
        tree = etree.parse(file)
        extracted_text = ''.join(tree.xpath('//text()'))
    
    return extracted_text

def process_ocr_to_general_structure(ocr_text):
    """ A generalized approach to extract key-value pairs from OCR text. """
    lines = ocr_text.split('\n')
    structured_data = {}

    current_key = None
    for line in lines:
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            structured_data[key.strip()] = value.strip()
        else:
            if current_key:
                structured_data[current_key] += f' {line.strip()}'
            else:
                # If no key is established, we skip the line
                continue

        if current_key is None:
            current_key = key.strip()  # Start with the first key found

    return json.dumps(structured_data, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            file_type = filename.rsplit('.', 1)[1].lower()
            if file_type in ['png', 'jpg', 'jpeg', 'gif']:
                extracted_text = process_image_with_ocr(file_path)
                structured_json = process_ocr_to_general_structure(extracted_text)
            elif file_type == 'pdf':
                extracted_text = process_pdf(file_path)
                structured_json = process_ocr_to_general_structure(extracted_text)
            elif file_type == 'docx':
                extracted_text = process_docx(file_path)
                structured_json = process_ocr_to_general_structure(extracted_text)
            elif file_type == 'xlsx':
                extracted_text = process_xlsx(file_path)
                structured_json = process_ocr_to_general_structure(extracted_text)
            elif file_type == 'json':
                structured_json = process_json(file_path)
                extracted_text = structured_json  # To return the raw JSON
            elif file_type == 'xml':
                structured_json = process_xml(file_path )
                extracted_text = structured_json  # To return the raw XML
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
                    structured_json = process_ocr_to_general_structure(extracted_text)
            
            return jsonify({
                'extracted_text': extracted_text,
                'structured_json': structured_json,
                'file_type': file_type
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        ocr_text = data.get('ocr_text', '')
        context = data.get('context', '')
        
        if not ocr_text:
            return jsonify({'error': 'No text provided for summarization'}), 400
        
        ocr_text = html.unescape(ocr_text)
        
        summary = summarize_text(ocr_text, context)
        polarity, subjectivity = analyze_sentiment(ocr_text)
        
        return jsonify({
            'summary': summary,
            'polarity': polarity,
            'subjectivity': subjectivity
        })
    
    except Exception as e:
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
