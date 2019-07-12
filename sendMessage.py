import requests  # send Message 요청을 하기 위한 모듈
import pprint
from decouple import config # decouple 에서부터 config 호출


base_url = 'https://api.telegram.org'
token = config('API_TOKEN')
chat_id = config('CHAT_ID')
text = 'decouple test'

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

response = requests.get(api_url) # requests 로 받은 응답을 response 로 받겠다
pprint.pprint(response.json())


