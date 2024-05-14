import os
from google.cloud import storage
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GCS_BUCKET_NAME = 'inf-bucket'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\marcl\Downloads\inf-bucket-a704026b6ec1.json"
storage_client = storage.Client()

def upload_file_to_gcs(file, filename):
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    return blob.public_url

def download_file_from_gcs(filename):
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    temp_filepath = os.path.join('/tmp', filename)
    
    if not os.path.exists('/tmp'):
        os.makedirs('/tmp')

    blob.download_to_filename(temp_filepath)
    return temp_filepath

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    filename = request.form.get('filename', file.filename)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        public_url = upload_file_to_gcs(file, filename)
        return jsonify({'message': 'File successfully uploaded', 'url': public_url}), 200
    except Exception as e:
        app.logger.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/download", methods=["POST"])
def download_from_bucket():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    try:
        destination_file_name = download_file_from_gcs(filename)
        return send_file(destination_file_name, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error downloading file: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
