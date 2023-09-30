from flask import Flask, request
import requests
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Чтение переменных окружения
TARGET_DOMAIN = os.environ.get('TARGET_DOMAIN', 'https://domain')
API_PREFIX = os.environ.get('API_PREFIX', '/api/')
LISTEN_PORT = int(os.environ.get('LISTEN_PORT', 8080))
CERT_PATH = os.environ.get('CERT_PATH', 'cert.pem')
KEY_PATH = os.environ.get('KEY_PATH', 'key.pem')

@app.route(f'{API_PREFIX}<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(subpath):
    target_url = f"{TARGET_DOMAIN}{API_PREFIX}{subpath}"

    # Логирование
    logging.info(f"Received API request: {request.method} {request.url}")

    # Проксирование запроса
    response = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        params=request.args,
        json=request.get_json() or request.form or None,
        cookies=request.cookies
    )

    # Возвращаем ответ
    return (response.content, response.status_code, response.headers.items())

DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

if __name__ == '__main__':
    if DEBUG_MODE:
        app.run(port=LISTEN_PORT, debug=True)
    else:
        app.run(port=LISTEN_PORT, ssl_context=(CERT_PATH, KEY_PATH))
