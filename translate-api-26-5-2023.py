from easygoogletranslate import EasyGoogleTranslate
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import json

app = Flask(__name__)



@app.route("/tran", methods=["GET"])
def DevseniorTranslate():
    devsenior_translate = request.headers.get('translate')
    lang_in = request.headers.get('langin')
    lang_out = request.headers.get('langout')
    print(devsenior_translate)
    translator = EasyGoogleTranslate(
        source_language = lang_in,
        target_language = lang_out,
        timeout=10
    )
    result = translator.translate(devsenior_translate)
    return  {"result" : result}
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1999)

