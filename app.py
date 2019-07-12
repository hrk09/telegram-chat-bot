from flask import Flask, request
from decouple import config
import requests
import pprint

app = Flask(__name__)
API_TOKEN = config('API_TOKEN')  # 상수는 대문자


@app.route('/')
def hello():
    return 'HelloWorld'

@app.route('/greeting/<name>')
def greeting(name):
    return f'Hello, {name}'

@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json()  # 보낸 메세지 정보가 감
    # pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None:
        # 우리가 원하는 로직
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')
        # print('chat_id : ', chat_id)
        # print('text : ', text)

        if text == 'ㅇㅅㅇ?':
            text = 'ㅇㅅㅇ!'
    
        # 받은 메세지를 보낸 사람한테 그대로 전달(Send Message Logic)
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)