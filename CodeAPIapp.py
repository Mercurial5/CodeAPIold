from flask import Flask, request
from dotenv import load_dotenv
from os import getenv

from utils import check

app = Flask(__name__)


@app.route('/run', methods=['POST'])
def run():
    data = request.form
    code = data.get('code', None)
    lang = data.get('lang', None)
    inputs = data.getlist('inputs')
    outputs = data.getlist('outputs')

    if not all([code, lang, inputs, outputs]):
        return dict(status=False, reason='Not all data was given')

    return check(code, lang, inputs, outputs)


if __name__ == '__main__':
    load_dotenv()
    app.run(host=getenv('host'), port=getenv('port'))
