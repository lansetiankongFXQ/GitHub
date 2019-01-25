# -*- coding:utf-8 -*-
import time
import sys
import os
sys.path.append(os.getcwd())
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from taodata.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME
from pymongo.errors import DuplicateKeyError
import pymongo
import traceback
import random

'''
极验验证码特点：首先点击按钮进行智能验证，如果验证不通过，则会弹出滑动验证的窗口，
拖动滑块拼合图像进行验证，之后生成三个加密参数，通过表单提交到后台，后台还会进行一次验证。
识别验证需要三步：
1.模拟点击验证按钮
2.识别滑动缺口的位置
3.模拟拖动滑块
'''

BORDER = 6


class CrackGeetest():
    def __init__(self, username, password):
        os.system('pkill -f phantom')
        service_args = [
            '--proxy=http://proxy.abuyun.com:9020',
            '--proxy-auth=HI1KUC7XVQ0249ZD:3E0AA3CE27CAB12F',
            '--ignore-ssl-errors=true'
        ]
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1050, 840)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def __del__(self):
        pass
        #self.browser.close()

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(random.uniform(0, 3))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_position1(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(random.uniform(0, 3))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)


    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_geetest_image1(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position1()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        email.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                        pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        distance = distance

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(random.uniform(0, 1))
        ActionChains(self.browser).release().perform()

    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'loginAction')))
        submit.click()
        time.sleep(random.uniform(5, 10))
        print('登录成功')

    def crack(self):
        # 输入用户名密码
        self.open()

        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()

        time.sleep(random.uniform(0, 3))
        fullbg = self.browser.find_element_by_class_name('geetest_canvas_fullbg')
        self.browser.execute_script('arguments[0].style.display="block"', fullbg)
        # 获取验证码图片
        image1 = self.get_geetest_image1('captcha1.png')
        self.browser.execute_script('arguments[0].style.display="none"', fullbg)
        time.sleep(random.uniform(0, 3))

        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        time.sleep(random.uniform(0, 3))
        slice = self.browser.find_element_by_class_name('geetest_canvas_slice')
        self.browser.execute_script('arguments[0].style.display="none"', slice)
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        self.browser.execute_script('arguments[0].style.display="block"', slice)

        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)

        success = self.wait.until_not(EC.title_contains('验证'))
        if success:
            cookies = self.browser.get_cookies()
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookie_str = '; '.join(item for item in cookie)
            self.browser.quit()
            print(cookie_str)
            return cookie_str
        else:
            return None


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
                        cookie_str = CrackGeetest(username, password).crack()
                    else:
                        print('ok-->已登录')
                        continue
                else:
                    cookie_str = CrackGeetest(username, password).crack()
            else:
                cookie_str = CrackGeetest(username, password).crack()
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