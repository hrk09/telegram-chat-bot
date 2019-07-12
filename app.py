from flask import Flask, request
from decouple import config
import requests
import pprint

app = Flask(__name__)

API_TOKEN = config('API_TOKEN')  # 상수는 대문자
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')

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

        # if text == 'ㅇㅅㅇ?':  # ㅇㅅㅇ? 라고 보내면 ㅇㅅㅇ!라고 답옴
        #     text = 'ㅇㅅㅇ!'
        
        if text[0:4] == '/영한 ':
            headers = { 
                'X-Naver-Client-Id': NAVER_CLIENT_ID,  # trailing comma ',' 찍어주는 것
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:] # '/번역' 이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)   
            text = papago_res.json().get('message').get('result').get('translatedText')


        if text[0:4] == '/한영 ':
            headers = { 
                'X-Naver-Client-Id': NAVER_CLIENT_ID,  # trailing comma ',' 찍어주는 것
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:] # '/번역' 이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)   
            text = papago_res.json().get('message').get('result').get('translatedText')        



        # 받은 메세지를 보낸 사람한테 그대로 전달(Send Message Logic)
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)