from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# GET semplice
@app.route('/', methods=['GET'])
def hello():
    return jsonify({"ciao": "swag"})

# POST semplice
@app.route('/echo', methods=['POST'])
def echo():
    data = request.json  # riceve JSON
    return jsonify({"received": data})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

