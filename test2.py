import requests
mobile = '19918316880'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
# 网易云游戏
data={
        "etc": {
            "validate": ""
        }
    }
sms_url = 'https://n.cg.163.com/api/v1/phone-captchas/86-' + mobile
sms_response = requests.post(url=sms_url,headers=headers,data=data)
print('[网易云游戏] 发送成功')