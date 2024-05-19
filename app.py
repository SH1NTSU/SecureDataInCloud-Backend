import os
from google.cloud import storage
from enc_and_dec.enc_and_dec_file import EncAndDecFile
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import psycopg2 

app = Flask(__name__)
CORS(app)

try:
    connection_string = "host=localhost port=5000 dbname=postgres user=postgres password=password connect_timeout=10 sslmode=prefer"
    print(connection_string)
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    print("Connection successful!")
except psycopg2.Error as e:
    print("Unable to connect to the database:", e)


CREATE_TABLE = """CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    name text NOT NULL, 
    key text NOT NULL
);"""
cur.execute(CREATE_TABLE)
conn.commit()
@app.route("/upload", methods=["POST"])
def upload_to_bucket():
    print(request)  
    file = request.files['file']
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})



    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    upload_dir = r'C:\Users\marcl\Projects\SecureDataInCloud-Backend'

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file.save(os.path.join(upload_dir, file.filename))

    encrypt = EncAndDecFile(file.filename).encrypt_file()
    key = encrypt[0]    
    encrypted_file = encrypt[1]
    print(encrypted_file, key)
    cur.execute("INSERT INTO files (name, key) VALUES (%s, %s)", (encrypted_file, key))
    conn.commit()
    blob_name = encrypted_file
    bucket_name = "inf-bucket"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\marcl\OneDrive\Documents\inf-bucket-29e11205031f.json"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(os.path.join(upload_dir, blob_name))
    return jsonify({'message': 'File uploaded successfully'})



@app.route("/download", methods=["POST"])
def download_from_bucket():
    body = request.get_json()
    file_name = body['filename']


    source_blob_name = f"enc_{file_name}"
    destination_file_name = source_blob_name
    bucket_name = "inf-bucket"
    print(source_blob_name)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\marcl\OneDrive\Documents\inf-bucket-29e11205031f.json"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    cur.execute("SELECT key FROM files WHERE name = %s", (file_name,))
    key = cur.fetchone()

    if not key:
        return jsonify({'error': 'No key found for file'})
    
    decoded_key = key.decode("utf-8")


    decrypted_file = EncAndDecFile(file_name).decrypt_file(decoded_key, source_blob_name)

    return decrypted_file.public_url


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
