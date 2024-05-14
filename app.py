import os
from google.cloud import storage
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_to_bucket():
    path_to_file = request.get_data()
    print(path_to_file)
    blob_name = "encrypted.txt"
    bucket_name = "inf-bucket"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\MarcelBudziszewski\Documents\inf-bucket-5c2b1ac1eb78.json"

    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)

        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
@app.route("/download", methods=["GET"])
def download_from_bucket():
    source_blob_name = "encrypted.txt"
    destination_file_name = r"C:\Users\MarcelBudziszewski\SecureDataInCloud-Backend\hei.txt"
    bucket_name = "inf-bucket"
    
  
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\MarcelBudziszewski\Documents\inf-bucket-5c2b1ac1eb78.json"

    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        return blob.public_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    app.run(host="localhost", port=5000)

