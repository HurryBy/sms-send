import sys
import requests
import time
try:
    mobile = sys.argv[1]
except:
    mobile = input('手机号:')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
def get_time():
    return str(int(time.time() * 1000))
# NN加速器
sms_url = 'https://opapi2.nn.com/u-mobile/sendSms'
data = {
    "countryCode" : 86,
    "telNum" : mobile
}
special_headers = {
    "token" : "600e862372974222bf1af8849f38fa28",
    "appId" : "nnMobileIm_6z0g3ut7",
    "timeStamp" : get_time(),
    "signType" : "1",
    "version" : "7",
    "reqChannel" : "2",
    "deviceId" : "7181d4fd37c1cb42",
    "appName" : "leigod_accelerator",
    "platform" : "2",
    "registerCanal": "common",
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": "41",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.9.2"
}
sms_response = requests.post(url=sms_url,headers=special_headers,data=data)
print('[NN加速器] ' + sms_response.text)
print(get_time())