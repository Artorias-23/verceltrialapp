from flask import Flask, request, jsonify, send_file, render_template
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from io import BytesIO
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend development

logging.basicConfig(level=logging.INFO)
app.logger.info("Merging PDFs...")
app.logger.error("Error while merging", exc_info=True)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    if len(files) < 2:
        return jsonify({'error': 'Need at least 2 PDFs to merge'}), 400

    merger = PdfMerger()
    for file in files:
        if file.filename.endswith('.pdf'):
            merger.append(file)

    output = BytesIO()
    merger.write(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='merged.pdf'
    )

@app.route('/split', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400

    reader = PdfReader(file)
    if len(reader.pages) < 1:
        return jsonify({'error': 'PDF has no pages'}), 400

    # For simplicity, we'll return the first page only
    writer = PdfWriter()
    writer.add_page(reader.pages[0])

    output = BytesIO()
    writer.write(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='page_1.pdf'
    )

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def catch_all(path):
    if path == "favicon.ico":
        return "", 404
    return render_template("index.html")

# if __name__ == '__main__':
#     app.run(debug=True)
