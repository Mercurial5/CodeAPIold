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
    input = data.get('input', None)
    output = data.get('output', None)
    io_count = data.get('io_count', None)
    io_tuple_count = data.get('io_tuple_count', None)

    if None in [code, lang, input, output, io_count, io_tuple_count]:
        return dict(status=False, reason='Not all data was given')

    return check(code, lang, input, output, io_count, io_tuple_count)


if __name__ == '__main__':
    load_dotenv()
    app.run(host=getenv('host'), port=getenv('port'))
