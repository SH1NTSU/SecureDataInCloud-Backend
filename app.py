from flask import Flask, request

app = Flask(__name__)

Api_key = "AIzaSyBjBPh9HEzxq_StM35Oy1ME1p0x1bYBU74"

@app.route('/encrypt')
def encrypt():
    body = request.get_data()
    encrypted_body = encrypt(body)
    


@app.route('/decrypt')
def decrypt():
    body = request.get_json()
    return body

if __name__ == '__main__':
    app.run(debug=True)


