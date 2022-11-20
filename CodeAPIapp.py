from flask import Flask, request
from dotenv import load_dotenv
from os import getenv

from utils import check_weak_samples, check_strong_samples

app = Flask(__name__)


@app.route('/run', methods=['POST'])
def run():
    data = request.form
    code = data.get('code', None)
    lang = data.get('lang', None)
    weak_inputs = data.getlist('weak_inputs')
    weak_outputs = data.getlist('weak_outputs')
    strong_inputs = data.getlist('strong_inputs')
    strong_outputs = data.getlist('strong_outputs')

    if not all([code, lang, weak_inputs, weak_outputs, strong_inputs, strong_outputs]):
        return dict(status=False, reason='Not all data was given')

    response = check_weak_samples(code, lang, weak_inputs, weak_outputs)
    if response['status']:
        # because first case in strong samples is not first case overall
        # (because first case was in weak samples) we need to add shift
        case_shift = len(weak_inputs)
        return check_strong_samples(code, lang, strong_inputs, strong_outputs, case_shift)

    return response


if __name__ == '__main__':
    load_dotenv()
    app.run(host=getenv('host'), port=getenv('port'))
