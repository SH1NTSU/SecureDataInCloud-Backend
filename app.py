import os
from google.cloud import storage
from enc_and_dec.enc_and_dec_file import EncAndDecFile
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import psycopg2
import base64

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
    name TEXT NOT NULL, 
    key TEXT NOT NULL
);"""
cur.execute(CREATE_TABLE)
conn.commit()


@app.route("/upload", methods=["POST"])
def upload_to_bucket():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    upload_dir = r"C:\Users\marcl\Projects\SecureDataInCloud-Backend"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    encrypt = EncAndDecFile(file.filename)
    key, encrypted_file = encrypt.encrypt_file()
    base64_key = base64.urlsafe_b64encode(key).decode("utf-8")

    cur.execute(
        "INSERT INTO files (name, key) VALUES (%s, %s)", (encrypted_file, base64_key)
    )
    conn.commit()

    blob_name = encrypted_file
    bucket_name = "inf-bucket"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        r"C:\Users\marcl\OneDrive\Documents\inf-bucket-29e11205031f.json"
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(os.path.join(upload_dir, blob_name))

    return jsonify({"message": "File uploaded successfully"})


@app.route("/download", methods=["POST"])
def download_from_bucket():
    body = request.get_json()
    file_name = body["filename"]

    source_blob_name = f"enc_{file_name}"
    destination_file_name = os.path.join(r"C:\Users\marcl\Downloads", source_blob_name)
    bucket_name = "inf-bucket"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        r"C:\Users\marcl\OneDrive\Documents\inf-bucket-29e11205031f.json"
    )

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    cur.execute("SELECT key FROM files WHERE name = %s", (source_blob_name,))
    data = cur.fetchone()
    if data is None:
        return jsonify({"error": "Key not found for file"}), 404

    base64_key = data[0]
    key = base64.urlsafe_b64decode(base64_key)

    try:
        decryptor = EncAndDecFile(file_name)
        decrypted_file = decryptor.decrypt_file(key, destination_file_name)
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return jsonify({"error": "Decryption failed"}), 500

    with open(decrypted_file, "rb") as file:
        content = file.read()

    return content


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
