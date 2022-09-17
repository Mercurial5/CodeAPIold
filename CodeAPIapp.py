from flask import Flask, request
from dotenv import load_dotenv
from os import getenv

from utils import check


app = Flask(__name__)


@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    code = data.get('code', None)
    lang = data.get('lang', None)
    io = data.get('io', None)

    if None in [code, lang, io]:
        return dict(status=False, reason='Not all data was given')

    return check(code, lang, io)


if __name__ == '__main__':
    load_dotenv()
    app.run(host=getenv('host'), port=getenv('port'))
