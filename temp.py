from flask import Flask, render_template, url_for, request, session, redirect, jsonify


import os
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def hello():
    if request.method == "POST":
        a = request.json
        print(a)
        values = a["hi"]
        os.system("say '" + values + "'")
    return "Hello"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6969)
