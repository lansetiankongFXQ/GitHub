import os
import time
from io import BytesIO
import pymongo
from PIL import Image
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
import sys
sys.path.append(os.getcwd())
from taodata.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME
import traceback

TEMPLATES_FOLDER = './taodata/account/weibo_cn/templates/'


class WeiboLogin():
    def __init__(self, username, password):
        os.system('pkill -f phantom')
        service_args = [
            '--proxy=http://proxy.abuyun.com:9020',
            '--proxy-auth=HI1KUC7XVQ0249ZD:3E0AA3CE27CAB12F',
            '--ignore-ssl-errors=true'
        ]
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        self.browser = webdriver.Chrome(service_args=service_args)
        self.browser.set_window_size(1050, 840)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        print('ok->open')
        submit.click()

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip_content')))
            element = self.browser.find_element_by_class_name('geetest_radar_tip_content')
            element.click()
            print('点击按钮进行验证')
            time.sleep(2)
        except TimeoutException:
            print('未出现点击按钮进行验证')

    def run(self):
        """
        破解入口
        :return:
        """
        self.open()
        print('打开登录页面')

        self.get_position()

        WebDriverWait(self.browser, 15).until_not(EC.title_contains('验证'))

        cookies = self.browser.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in cookies]
        cookie_str = '; '.join(item for item in cookie)
        print(cookie_str)
        self.browser.quit()
        return cookie_str


if __name__ == '__main__':
    file_path = r'./taodata/account/weibo_cn/account_prod.txt'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    mongo_client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
    collection = mongo_client[DB_NAME]["account"]
    for line in lines:
        line = line.strip()
        username = line.split('----')[0]
        password = line.split('----')[1]
        print('=' * 10 + username + '=' * 10)
        try:
            users = collection.find_one({'_id': username})
            if users:
                user = users
                if user:
                    status = user['status']
                    if 'error' == status:
                        cookie_str = WeiboLogin(username, password).run()
                    else:
                        print('ok-->已登录')
                        continue
                else:
                    cookie_str = WeiboLogin(username, password).run()
            else:
                cookie_str = WeiboLogin(username, password).run()
        except Exception as e:
            print('获取cookie异常')
            traceback.print_exc()
            continue
        if cookie_str and len(cookie_str) > 0:
            print('获取cookie成功')
        else:
            print('获取cookie失败')
            continue
        try:
            collection.insert({"_id": username, "password": password, "cookie": cookie_str, "status": "success"})
        except DuplicateKeyError as e:
            collection.find_one_and_update({'_id': username}, {'$set': {'cookie': cookie_str, "status": "success"}})


