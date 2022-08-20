import time
import os
import sys
import json
import requests
from PIL import Image
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
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
my_share = share.Share('7974.T')
symbol_data = None
 
try:
    yahoo = my_share.get_historical(share.PERIOD_TYPE_DAY, 2, share.FREQUENCY_TYPE_DAY, 1)
    today = round(yahoo["close"][1], 2)
    yesterday = round(yahoo["close"][0], 2)
    ratio = round(today - yesterday, 2)
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)
 
print(yahoo)
print(ratio)

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
windowSizeHeight = 1600
#windowWidth = windowSizeWidth if windowSizeWidth else driver.execute_script('return document.body.scrollWidth;')
#windowHeight = windowSizeHeight if windowSizeHeight else driver.execute_script('return document.body.scrollHeight;')
driver.set_window_size(windowSizeWidth, windowSizeHeight)

# 処理後一時待機,スクリーンショット格納,ブラウザ稼働終了
time.sleep(2)
driver.save_screenshot('image.png')
time.sleep(1)
driver.quit()

#--------------------------------------------------------------------------------------------------------------------------------------
text = '今日の' + 'test' + 'の株価は' + str(today) + 'ドル' + 'で、前日比は' + str(ratio) + 'です。'
content = {'content': text}
headers = {'Content-Type': 'application/json'}
with open('image.png', 'rb') as f:
    file_bin = f.read()
image = {'upload' : ('image.png', file_bin)}
response = requests.post(webhook_url, json.dumps(content), headers=headers)
response = requests.post(webhook_url, files = image)
