import time
import sys
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
#株価取得
my_share = share.Share('MSFT')
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
driver.get("https://www.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_indexDetail&cat1=market&cat2=index&dir=tl1-idxdtl%7Ctl2-.N225%7Ctl5-jpn&file=index.html&getFlg=on")
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
  
# ウインドウ幅・高さ指定
windowSizeWidth = 800
windowSizeHeight = 600
windowWidth = windowSizeWidth if windowSizeWidth else driver.execute_script('return document.body.scrollWidth;')
windowHeight = windowSizeHeight if windowSizeHeight else driver.execute_script('return document.body.scrollHeight;')
driver.set_window_size(windowWidth, windowHeight)

# 処理後一時待機,スクリーンショット格納,ブラウザ稼働終了
time.sleep(2)
driver.save_screenshot('image.png')
time.sleep(1)
driver.quit()
