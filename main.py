import time
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#--------------------------------------------------------------------------------------------------------------------------------------
webhook_url = os.environ.get("WEBHOOK")
abc = "7974:TYO"
#--------------------------------------------------------------------------------------------------------------------------------------
#株価取得
url = "https://finance.yahoo.co.jp/quote/7974.T"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
rs = soup.find(class_='_3rXWJKZF')
rs = [i.strip() for i in rs.text.splitlines()]
rs = [i for i in rs if i != ""]
today = rs[0]
rs = soup.find(class_='_1-yujUee Y_utZE_b')
rs = [i.strip() for i in rs.text.splitlines()]
rs = [i for i in rs if i != ""]
ratio = rs[0]

#--------------------------------------------------------------------------------------------------------------------------------------
# Chromeヘッドレスモード起動
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10)

# サイトURL取得
driver.get("https://www.google.com/finance/quote/" + abc + "?hl=ja&gl=JP&window=1M")
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
  
# ウインドウ幅・高さ指定
windowSizeWidth = 800
windowSizeHeight = 600
#windowWidth = windowSizeWidth if windowSizeWidth else driver.execute_script('return document.body.scrollWidth;')
#windowHeight = windowSizeHeight if windowSizeHeight else driver.execute_script('return document.body.scrollHeight;')
driver.set_window_size(windowSizeWidth, windowSizeHeight)

# 処理後一時待機,スクリーンショット格納,ブラウザ稼働終了
time.sleep(2)
driver.save_screenshot('before.png')
time.sleep(1)
driver.quit()

# 画像トリミング
im = Image.open('before.png')
im.crop((0, 110, 770, 550)).save('image.png', quality=95)

#--------------------------------------------------------------------------------------------------------------------------------------
text = '今日の' + 'test' + 'の株価は' + str(today) + 'ドル' + 'で、前日比は' + str(ratio) + 'でした。'
content = {'content': text}
headers = {'Content-Type': 'application/json'}
with open('image.png', 'rb') as f:
    file_bin = f.read()
image = {'upload' : ('image.png', file_bin)}
response = requests.post(webhook_url, json.dumps(content), headers=headers)
response = requests.post(webhook_url, files = image)
