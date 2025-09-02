from flask import Flask, request, jsonify, render_template, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<string:name>')
def page(name):
    path = os.path.join(app.template_folder, f"{name}.html")
    if os.path.exists(path):
        return render_template(f"{name}.html")
    else:
        abort(404)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

