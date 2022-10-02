from threading import Thread, current_thread
from lxml import etree
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import requests
import cv2
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
def get_time():
    return str(int(time.time() * 1000))
def get_pos(image,a,b,c,d):
    blurred = cv2.GaussianBlur(image, (5, 5), 0,0)
    canny = cv2.Canny(blurred, 200, 400)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours, hierarchy)
    for i, contour in enumerate(contours):
        M = cv2.moments(contour)
        if M['m00'] == 0:
            cx = cy = 0
        else:
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
        if a < cv2.contourArea(contour) < b and c < cv2.arcLength(contour, True) < d:
            if cx < 400:
                continue
            print(cv2.contourArea(contour))
            print(cv2.arcLength(contour, True))
            x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv2.imshow('image', image)
            # cv2.imwrite('111.jpg', image)
            return x
    return 0
try:
    mobile = sys.argv[1]
    count = sys.argv[2]
except:
    mobile = input('手机号:')
    count = input('次数:')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
def selenium_auto_process():
    for counted in range(int(count)):
        # ===================================selenium auto process===================================
        driver = webdriver.Chrome()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
        })
        driver.set_page_load_timeout(20)
        
        # 53kf
        try:
            driver.get('https://www.53kf.com/reg/index')
        except:
            pass
        time.sleep(0.4)
        driver.find_element(By.ID,'phone').send_keys(mobile)
        time.sleep(0.4)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.CLASS_NAME,'get-yzm')))
        driver.find_element(By.CLASS_NAME,'get-yzm').click()
        time.sleep(1)

        # pfcexpress
        try:
            driver.get('https://www.pfcexpress.com/Manage/WebManage/NewRegister.aspx')
        except:
            pass
        driver.find_element(By.XPATH,'//*[@id="PhoneNO"]').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="getVeri"]')))
        driver.find_element(By.XPATH,'//*[@id="getVeri"]').click()
        time.sleep(1)

        driver.get('https://ts.voc.com.cn/user/register.html')
        time.sleep(2)
        driver.find_element(By.ID,'js-mobile-input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[5]/div[2]/form/dl/div[1]/dd/button')))
        driver.find_element(By.XPATH,'/html/body/div[1]/div[5]/div[2]/form/dl/div[1]/dd/button').click()
        time.sleep(2)
        driver.switch_to.frame('tcaptcha_iframe')
        while True:
            time.sleep(2)
            verify_img = driver.find_element(By.XPATH,'//*[@id="slideBg"]')
            img_url = verify_img.get_attribute('src')
            print(img_url)
            content = requests.get(url=img_url).content
            with open("verify_img.jpg" , 'wb') as f:
                f.write(content)
            verify_img = cv2.imread('verify_img.jpg')
            x = get_pos(verify_img,6000,8000,370,390)
            result = int(x * 0.41) + 3
            slide = driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]')
            actions = webdriver.ActionChains(driver)
            actions.drag_and_drop_by_offset(slide,result, 0).perform()
            driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]').click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH,'//*[@id="reload"]/div').click()
            except: 
                break
        time.sleep(1)

        # chinamendu
        driver.get('http://www.chinamendu.com/Register.aspx')
        time.sleep(2)
        driver.find_element(By.ID,'txtMobile').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/form/div[3]/div[2]/div[1]/div[6]/div/span[1]')))
        driver.find_element(By.XPATH,'/html/body/form/div[3]/div[2]/div[1]/div[6]/div/span[1]').click()
        time.sleep(2)
        driver.switch_to.frame('tcaptcha_iframe')
        while True:
            time.sleep(2)
            verify_img = driver.find_element(By.XPATH,'//*[@id="slideBg"]')
            img_url = verify_img.get_attribute('src')
            print(img_url)
            content = requests.get(url=img_url).content
            with open("verify_img.jpg" , 'wb') as f:
                f.write(content)
            verify_img = cv2.imread('verify_img.jpg')
            x = get_pos(verify_img,6000,8000,370,390)
            result = int(x * 0.41) + 3
            slide = driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]')
            actions = webdriver.ActionChains(driver)
            actions.drag_and_drop_by_offset(slide,result, 0).perform()
            driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]').click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH,'//*[@id="reload"]/div').click()
            except: 
                break
        time.sleep(1.5)
        try:
            dig_alert = driver.switch_to.alert
            dig_alert.accept()
        except:
            pass
        time.sleep(1)

        # 95bd
        driver.get('https://www.95bd.com/passport-signup.html')
        driver.find_element(By.ID,'mobile').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.ID,'resend')))
        driver.find_element(By.ID,'resend').click()
        time.sleep(1.5)
        try:
            dig_alert = driver.switch_to.alert
            dig_alert.accept()
        except:
            pass
        time.sleep(1)

        # qncyw
        driver.get('https://qncyw.com/site/signup')
        driver.find_element(By.ID,'username').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.ID,'btnSendCode')))
        driver.find_element(By.ID,'btnSendCode').click()
        time.sleep(1.5)
        try:
            warn_alert = driver.switch_to.alert
            warn_alert.accept()
        except:
            pass
        time.sleep(1)

        # acfun
        driver.get('https://www.acfun.cn/reg/')
        driver.find_element(By.XPATH,'/html/body/div/div/main/div/div[2]/div/div[2]/form/div[1]/span/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div/div/main/div/div[2]/div/div[2]/form/div[4]/span/div[2]/span')))
        driver.find_element(By.XPATH,'/html/body/div/div/main/div/div[2]/div/div[2]/form/div[4]/span/div[2]/span').click()
        time.sleep(1)

        # iwgame
        driver.get('https://passport.iwgame.com/reg/account/regpage.do')
        driver.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/form/ul/li[1]/div[1]/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div/div[2]/form/ul/li[5]/div[1]/em/a')))
        driver.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/form/ul/li[5]/div[1]/em/a').click()
        time.sleep(1)

        # ztgame
        driver.get('http://reg.ztgame.com/')
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/form/div[1]/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/div/div/form/div[2]/input[2]')))
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/form/div[2]/input[2]').click()
        time.sleep(1)

        # iprbase
        driver.get('http://www.iprbase.com/register')
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[1]/div[2]/form[1]/div[1]/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/div/div[1]/div[2]/form[1]/div[2]/div/div/a')))
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[1]/div[2]/form[1]/div[2]/div/div/a').click()
        time.sleep(1)

        # kuaidi100
        driver.get('https://sso.kuaidi100.com/sso/reg.jsp')
        driver.find_element(By.XPATH,'/html/body/div[2]/form/div[1]/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div[2]/form/div[3]/a')))
        driver.find_element(By.XPATH,'/html/body/div[2]/form/div[3]/a').click()
        time.sleep(1)

        # tangeche
        driver.get('https://www.tangeche.com/')
        driver.find_element(By.XPATH,'/html/body/div/div[2]/section[1]/div[3]/div/div[2]/div[1]/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/section[1]/div[3]/div/div[2]/div[2]')))
        driver.find_element(By.XPATH,'/html/body/div/div[2]/section[1]/div[3]/div/div[2]/div[2]').click()
        time.sleep(1)

        # shujuju
        driver.get('http://www.shujuju.cn/register')
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/form/div[1]/input').send_keys('HurryOS')
        time.sleep(0.2)
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/form/div[2]/input').send_keys(mobile)
        time.sleep(0.2)
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/form/div[4]/input').send_keys('.ky7r9f7d...')
        time.sleep(0.2)
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/form/div[5]/input').send_keys('.ky7r9f7d...')
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div/div[2]/div/form/div[6]/div/button')))
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/form/div[6]/div/button').click()
        time.sleep(1)

        # ggo
        driver.get('https://i.ggo.net/reg/index/referer=https%253A%252F%252Fmail.ggo.net')
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/ul/li[1]/input').send_keys(mobile)
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div[2]/ul/li[2]/a')))
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/ul/li[2]/a').click()
        time.sleep(2)
        driver.switch_to.frame('tcaptcha_iframe')
        while True:
            time.sleep(2)
            verify_img = driver.find_element(By.XPATH,'//*[@id="slideBg"]')
            img_url = verify_img.get_attribute('src')
            print(img_url)
            content = requests.get(url=img_url).content
            with open("verify_img.jpg" , 'wb') as f:
                f.write(content)
            verify_img = cv2.imread('verify_img.jpg')
            x = get_pos(verify_img,6000,8000,370,390)
            result = int(x * 0.41) + 3
            slide = driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]')
            actions = webdriver.ActionChains(driver)
            actions.drag_and_drop_by_offset(slide,result, 0).perform()
            driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]').click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH,'//*[@id="reload"]/div').click()
            except: 
                break
        time.sleep(1)

        # spbspb
        driver.get('https://www.spb.cn/index.php/user/reg')
        driver.find_element(By.XPATH,'//*[@id="usertel"]').send_keys(mobile)
        time.sleep(0.2)
        driver.find_element(By.XPATH,'//*[@id="userpass"]').send_keys('.ky7r9f7d...')
        time.sleep(0.2)
        driver.find_element(By.XPATH,'//*[@id="mobie"]/table/tbody/tr[3]/td/input').send_keys('.ky7r9f7d...')
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="getcode"]')))
        driver.find_element(By.XPATH,'//*[@id="getcode"]').click()
        try:
            warn_alert = driver.switch_to.alert
            warn_alert.accept()
        except:
            pass
        time.sleep(1)

        # shuhai
        driver.get('http://www.shuhai.com/register')
        driver.find_element(By.XPATH,'//*[@id="mobile"]').send_keys(mobile)
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="getcode"]')))
        driver.find_element(By.XPATH,'//*[@id="getcode"]').click()
        try:
            warn_alert = driver.switch_to.alert
            warn_alert.accept()
        except:
            pass
        time.sleep(1)

        # mirxiaoyu
        driver.get('http://www.mirxiaoyu.com/jingdian/user/regmobile.html')
        driver.find_element(By.XPATH,'//*[@id="account"]').send_keys(mobile)
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="captcha"]/div[3]/div[2]/div[1]/div[3]')))
        driver.find_element(By.XPATH,'//*[@id="captcha"]/div[3]/div[2]/div[1]/div[3]').click()
        time.sleep(1.5)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="sendcode"]/a')))
        driver.find_element(By.XPATH,'//*[@id="sendcode"]/a').click()
        time.sleep(1)

        # cnki
        driver.get('https://wh.cnki.net/user/register')
        driver.find_element(By.XPATH,'//*[@id="phoneNum"]').send_keys(mobile)
        time.sleep(0.2)
        driver.find_element(By.XPATH,'//*[@id="psw"]').send_keys('.ky7r9f7d...')
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="sendCaptcha"]')))
        driver.find_element(By.XPATH,'//*[@id="sendCaptcha"]').click()
        time.sleep(1)

        # ngx
        driver.get('https://passport.ngx.net.cn/user/register.do?target=')
        driver.find_element(By.XPATH,'//*[@id="mobile"]').send_keys(mobile)
        time.sleep(0.2)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="sendCodeBtn"]')))
        driver.find_element(By.XPATH,'//*[@id="sendCodeBtn"]').click()
        time.sleep(1)

        # jlc
        driver.get('https://passport.jlc.com/register')
        driver.find_element(By.XPATH,'//*[@id="phoneNumber"]').send_keys(mobile)
        time.sleep(0.2)
        slide = driver.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
        actions = webdriver.ActionChains(driver)
        actions.click_and_hold(slide)
        actions.pause(0.2)
        actions.move_by_offset(440,0)
        actions.pause(0.2)
        actions.release()
        actions.click(slide)
        actions.perform()
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="sendBtn"]')))
        driver.find_element(By.XPATH,'//*[@id="sendBtn"]').click()
        time.sleep(2)
        try:
            warn_alert = driver.switch_to.alert
            warn_alert.accept()
        except:
            pass
        time.sleep(1)

        # tansoole
        driver.get('https://www.tansoole.com/reg/toReg.htm')
        driver.find_element(By.XPATH,'//*[@id="PlatformProBtn"]/a').click()
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="txt_mobile"]').send_keys(mobile)
        time.sleep(0.4)
        slide = driver.find_element(By.XPATH,'//*[@id="drag"]/div[3]')
        actions = webdriver.ActionChains(driver)
        actions.click_and_hold(slide)
        actions.pause(0.2)
        actions.move_by_offset(440,0)
        actions.pause(0.2)
        actions.release()
        actions.click(slide)
        actions.perform()
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="div_step_1_next"]')))
        driver.find_element(By.XPATH,'//*[@id="div_step_1_next"]').click()
        time.sleep(1.5)
        try:
            warn_alert = driver.switch_to.alert
            warn_alert.accept()
        except:
            pass
        time.sleep(1)
        
        # 湖南电信视频彩铃
        driver.get('https://web.jueywo.com/np-784940-101163/index.html?brandName=Other&a_slotId=400114&a_cid=31929241595&a_tuiaId=taw-10737365131921019&a_deviceId=479b8d18-1c2f-496e-a7c3-815563284642&a_appId=82738&userId=null&a_oId=taw-10737365131921019&flowId=cfcd208495d565ef66e7dff9f98764da&flowTagId=cfcd208495d565ef66e7dff9f98764da')
        time.sleep(1.5)
        driver.find_element(By.XPATH,'//*[@id="app"]/div[6]/div[1]/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[6]/div[1]/img')))
        driver.find_element(By.XPATH,'//*[@id="app"]/div[6]/div[1]/img').click()
        time.sleep(1)

        # 网易邮箱
        driver.get('http://zc.reg.163.com/regInitialized?#/')
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div[1]/input').send_keys('HurryOSZ8282')
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/input').send_keys('Hurry20070907.')
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div/div').click()
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/button').click()
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/input').send_keys(mobile)
        time.sleep(0.4)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/button').click()
        time.sleep(0.4)

        # 360账号注册
        driver.get('https://i.360.cn/reg/')
        time.sleep(1.5)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/div[1]/div/div[1]/div/div/div[2]/input').send_keys(mobile)
        time.sleep(0.4)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/div[1]/div/div[4]/div/div/div[2]/span').click()
        time.sleep(1.5)
        while True:
            while True:
                time.sleep(0.2)
                verify_img = driver.find_element(By.XPATH,'//*[@id="js-sdk"]/div/div[2]/div/div[1]/div/form/div[1]/div/div[3]/div/div[1]/div/div[1]/img[1]')
                img_url = verify_img.get_attribute('src')
                print(img_url)
                content = requests.get(url=img_url).content
                with open('verify_img.jpg','wb') as f:
                    f.write(content)
                verify_img = cv2.imread('verify_img.jpg')
                x=get_pos(verify_img,6000,10000,200,410)
                result = int(x * 0.51) - 1
                if(x == 0):
                    try:
                        driver.find_element(By.XPATH,'//*[@id="js-sdk"]/div/div[2]/div/div[1]/div/form/div[1]/div/div[3]/div/div[1]/div/div[1]/div[1]').click()
                    except:
                        driver.find_element(By.XPATH,'//*[@id="js-sdk"]/div/div[2]/div/div[1]/div/form/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]').click()
                        time.sleep(0.2)
                        driver.find_element(By.XPATH,'//*[@id="js-sdk"]/div/div[2]/div/div[1]/div/form/div[1]/div/div[3]/div/div[1]/div/div[1]/div[1]').click()
                else:
                    break
            slider = driver.find_element(By.XPATH,'//*[@id="js-sdk"]/div/div[2]/div/div[1]/div/form/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]')
            actions = webdriver.ActionChains(driver)
            actions.click_and_hold(slider)
            actions.pause(0.4)
            actions.move_by_offset(result,0)
            actions.pause(0.6)
            actions.release()
            actions.perform()
            actions.click(slider)
            time.sleep(1)
            try:
                driver.find_element(By.XPATH,'//*[@id="js-sdk"]/div/div[2]/div/div[1]/div/form/div[1]/div/div[3]/div/div[1]/div/div[1]/div[1]').click()
            except:
                break
        time.sleep(1)
        # 彩云
        driver.get('http://caiyunapp.com/user/login/')
        driver.find_element(By.XPATH,'//*[@id="phonenum"]').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="second"]')))
        driver.find_element(By.XPATH,'//*[@id="second"]').click()
        time.sleep(1)

        # PHP中文网
        driver.get('https://m.php.cn/login')
        driver.find_element(By.XPATH,'//*[@id="telphone_login"]').send_keys(mobile)
        time.sleep(0.2)
        slide = driver.find_element(By.XPATH,'//*[@id="verifysilide"]/div/div/div')
        actions = webdriver.ActionChains(driver)
        actions.click_and_hold(slide)
        actions.pause(0.2)
        actions.move_by_offset(574,0)
        actions.pause(0.2)
        actions.release()
        actions.click(slide)
        actions.perform()
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="user_phone_code_button"]')))
        driver.find_element(By.XPATH,'//*[@id="user_phone_code_button"]').click()
        time.sleep(1)

        # 码云社
        driver.get('https://www.codeseeding.com/index')
        driver.find_element(By.XPATH,'/html/body/header/div/div/div[1]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="loginModel"]/div/div[3]/p').click()
        time.sleep(0.2)
        driver.find_element(By.XPATH,'//*[@id="reg-phone"]').send_keys(mobile)
        time.sleep(0.1)
        driver.find_element(By.XPATH,'//*[@id="re-getCode"]').click()
        time.sleep(1)

        # 爱发电
        driver.get('https://afdian.net/login?type=mobile')
        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/section[1]/section/div[1]/div/div/input').send_keys(mobile)
        btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[1]/div/section[1]/section/div[2]/div[1]')))
        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/section[1]/section/div[2]/div[1]').click()
        time.sleep(1)

        driver.get('https://www.baidu.com/')
        driver.quit()
        driver.close()
        for timewaitcount in range(20):
            print('[' + current_thread().getName() + '] 正在等待 (' + str(timewaitcount) + ') 秒')
            time.sleep(1)
# ===Main===

plus = Thread(target=selenium_auto_process)
plus.start()