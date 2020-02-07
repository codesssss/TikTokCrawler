import io
import os
import sys

import appium
import goto
import selenium
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime
import random
from goto import with_goto

# 使用前请先在控制台输入:
# 'adb uninstall io.appium.uiautomator2.server'
# 'adb uninstall io.appium.uiautomator2.server.test'
# 同时在手机中卸载appium setting

# 目前代码用于已登录账户的软件

# 全局变量
platform = 'Android'
deviceName = 'VIE_AL10'  # 改成自己手机型号
app_package = 'com.ss.android.ugc.aweme.lite'
app_activity = 'com.ss.android.ugc.aweme.main.MainActivity'
driver_server = 'http://localhost:4723/wd/hub'
no_reset = True

screen_width = 0
screen_height = 0

flag_box = False
start_time_box = 0

flag_sign_in = False
time_sign_in = 0

now_day = 0


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


class TikTokCrawl():
    def __init__(self):
        self.desired_caps = {
            'platformName': platform,
            'deviceName': deviceName,
            'appPackage': app_package,
            'appActivity': app_activity,
            'noReset': no_reset
            # "unicodeKeyboard":True,
            # "resetKeyboard":True
        }
        self.driver = webdriver.Remote(driver_server, self.desired_caps)
        self.wait = WebDriverWait(self.driver, 300)
        self.always_allow(self.driver)

    # 用于同意系统权限
    def always_allow(self, driver, number=5):
        for i in range(number):
            loc = ("xpath", "//*[@text='我知道了']")
            try:
                e = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except:
                pass

    # 点亮红心
    def like(self):
        try:
            # el1 = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/a4m")
            # 第一种：直接点击两下
            # self.driver.tap([(1/2*screen_width-10, 1/2*screen_height-10), (1/2*screen_width+10, 1/2*screen_height+10)], 10)
            # self.driver.tap([(1 / 2 * screen_width - 10, 1 / 2 * screen_height - 10),
            #                  (1 / 2 * screen_width + 10, 1 / 2 * screen_height + 10)], 10)
            # 第二种：获取红心控件之后点击控件
            # self.driver.tap([(898/1812*screen_width, 743/1080*screen_height),(1078/1812*screen_width, 914/1080*screen_height)],100)

            # 第三种：直接点击控件
            # start = time.time()
            el1 = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/a4m")
            el1.click()
        except os.io.appium.uiautomator2.common.exceptions.ElementNotFoundException:
            print("未找到红心标志")
        # end = time.time()
        # print(end - start)

    # 下滑至下个视频
    def move_to_next(self):
        self.driver.swipe(1 / 2 * screen_width, 6 / 7 * screen_height, 1 / 2 * screen_width, 1 / 7 * screen_height, 500)

    # 上滑至上个视频
    def move_to_pre(self):
        self.driver.swipe(1 / 2 * screen_width, 1 / 7 * screen_height, 1 / 2 * screen_width, 6 / 7 * screen_height, 500)

    # 获取分辨率
    def get_width_height(self):
        global screen_height, screen_width
        # 获取屏幕的高
        screen_width = self.driver.get_window_size()['width']
        # 获取屏幕宽
        screen_height = self.driver.get_window_size()['height']

    # 进入赚金币界面
    def get_treasure(self):
        try:
            loc_treasure_entrance = ("xpath",
                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.TabHost/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout[3]")
            treasure_enter = WebDriverWait(self.driver, 1, 10).until(
                EC.presence_of_element_located(loc_treasure_entrance))
            treasure_enter.click()
        except os.io.appium.uiautomator2.common.exceptions.ElementNotFoundException:
            print("未找到赚金币入口")

    # 领取宝箱
    def get_treasure_box(self):
        try:
            loc_treasure_box = ("xpath",
                                '//android.widget.Image[@content-desc="开宝箱得金币"]')
            treasure_box = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(loc_treasure_box))
            treasure_box.click()
        except os.io.appium.uiautomator2.common.exceptions.ElementNotFoundException:
            print("未找到宝箱")

    # 退出赚金币界面
    def quit_treasure(self):
        try:
            quit_treasure = self.wait.until(
                EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme.lite:id/yt')))
            quit_treasure.click()
        except appium.uiautomator2.common.exceptions.ElementNotFoundException:
            print("退出赚金币界面失败")

    # 退出每日签到(弃用)
    def quit_sign_in(self):
        loc_sign_in = ("xpath",
                       ' //android.view.View[@content-desc="好的"]')
        sign_in = WebDriverWait(self.driver, 1, 10).until(EC.presence_of_element_located(loc_sign_in))
        sign_in.click()

    # 登陆账户
    def login(self):
        print("开始登录——————————")
        # 等待页面加载
        time.sleep(1)
        # 点开红包
        red_package = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/ahp")
        red_package.click()
        # 选赚更多
        earn_more = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme.lite:id/agv')))
        earn_more.click()
        # 同意条款
        agree_protocol = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme.lite:id/ae0')))
        agree_protocol.click()
        # 其他手机号码登陆
        loc_other = ("xpath",
                     " / hierarchy / android.widget.FrameLayout / android.widget.LinearLayout / android.widget.FrameLayout / android.widget.LinearLayout[1] / android.widget.FrameLayout / android.view.ViewGroup / android.widget.LinearLayout[2] / android.widget.LinearLayout")
        log_in_other = WebDriverWait(self.driver, 1, 10).until(EC.presence_of_element_located(loc_other))
        log_in_other.click()
        # 读取手机号
        phone_num = input('请输入手机号：\n格式：xxxxxxxxxxx\n')
        i = 0
        while i <= 10:
            self.driver.press_keycode((int)(phone_num[i]) + 7)
            i += 1
        # 利用模拟按键来解决输入位数的问题

        set_phone_num = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/a9l")
        set_phone_num.click()

        # 获取验证码
        get_verify = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/ae0")
        get_verify.click()
        enter_verify = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/ae9")
        verify_number = input("请输入验证码：\n")
        enter_verify.send_keys(verify_number)
        log_in_final = self.driver.find_element_by_id("com.ss.android.ugc.aweme.lite: id / a9l")
        log_in_final.click()
        # 赚更多
        earn_more = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme.lite:id/agu')))
        earn_more.click()
        # 跳过指导
        step_main = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme.lite:id/a3y')))
        step_main.click()


# @with_goto
def do_crawl(crawl):
    try:
        global start_time_box, now_day
        print("获取当前日期——————————")
        now_day = datetime.datetime.now().day
        # crawl.login()
        # time.sleep(3)
        print("获取分辨率——————————")
        crawl.get_width_height()
        print("长度为：", screen_height, "\n", "宽度为：", screen_width)
        crawl.driver.close_app()
        crawl.driver.launch_app()
        start_time_box = time.time()
        while True:
            print("正在检验日期是否变化——————————")
            day = datetime.datetime.now().day
            if day != now_day:
                print("变化，前去签到")
                now_day = day
                crawl.get_treasure()
                crawl.quit_treasure()
                print("签到完成！")
            else:
                print("未变化，正常进行")
            print("正在检验领取宝箱时间是否足够——————————")
            print("经过了", time.time() - start_time_box, "秒")
            if time.time() - start_time_box >= 3600:
                print("足够，前去领取")
                crawl.get_treasure()
                crawl.get_treasure_box()
                crawl.quit_treasure()
                print("领取成功！")
                start_time_box = time.time()
            else:
                print("不足，正常进行")
            choose_like = random.randint(1, 9)
            choose_view = random.randint(8, 15)
            crawl.move_to_next()
            print("下滑至下一个作品——————————")
            if choose_like / 9 == 0:
                print("随机喜欢了一个作品——————————")
                crawl.like()
            else:
                time.sleep(choose_view)
            print("观看了作品", choose_view, "秒")
    except selenium.common.exceptions.WebDriverException:
        print("服务器连接出错，尝试重启软件")
        time.sleep(1000)
        crawl.driver.close_app()
        crawl.driver.launch_app()
        # goto.rerun
        do_crawl(crawl)


if __name__ == '__main__':
    crawl = TikTokCrawl()
    do_crawl(crawl)
