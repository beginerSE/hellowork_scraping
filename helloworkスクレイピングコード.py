from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import re
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary 
import subprocess
import requests
import pandas as pd

url = "https://www.hellowork.mhlw.go.jp/"

cmd = 'pip install --upgrade chromedriver_binary' 
res = subprocess.call(cmd, shell=True) 
driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.get(url)
time.sleep(1)

driver.find_element_by_class_name("retrieval_icn").click()
time.sleep(1)

element = driver.find_element_by_id("ID_tDFK1CmbBox")
Select(element).select_by_value("13") #東京
time.sleep(1)

buttons = driver.find_elements_by_css_selector("input.button");
buttons[1].click()
time.sleep(1)

element = driver.find_element_by_id("ID_rank1CodeMulti")

Select(element).select_by_value("13119") #板橋区
Select(element).select_by_value("13120") #練馬区
Select(element).select_by_value("13121") #足立区
Select(element).select_by_value("13118") #荒川区
Select(element).select_by_value("13117") #北区
time.sleep(1)

driver.find_element_by_id("ID_ok").click()
time.sleep(1)

buttons = driver.find_elements_by_css_selector("input.button");
buttons[7].click()
time.sleep(1)

element = driver.find_element_by_id("ID_rank00Code")

#「E サービスの職業」を選択
Select(element).select_by_value("E")

#「下位」をクリック
driver.find_element_by_id("ID_down").click()
time.sleep(1)

#「下位」のドロップダウンリストを選択
element = driver.find_element_by_id("ID_rank00Code")

#「36 介護サービスの職業」を選択
Select(element).select_by_value("36")

#「下位」をクリック
driver.find_element_by_id("ID_down").click()
time.sleep(1)

#「下位」のドロップダウンリストを選択
element = driver.find_element_by_id("ID_rank00Code")

#「361 施設介護員」を選択
Select(element).select_by_value("361")

#「下位」をクリック
driver.find_element_by_id("ID_down").click()
time.sleep(3)

#「36101 施設介護員」が既に選択されているので、「決定」をクリック
driver.find_element_by_id("ID_ok").click()
time.sleep(3)

#「検索」をクリック
driver.find_element_by_id("ID_searchBtn").click()
time.sleep(3)

#「表示件数」ドロップダウンリストをクリック
element = driver.find_element_by_id("ID_fwListNaviDispBtm")

#「50件」を選択
Select(element).select_by_value("50")
time.sleep(5)

# 検索件数を取得
result_count = driver.find_elements_by_xpath('/html/body/div/div/form/div[6]/div[1]/div/span')
print('検索結果件数', result_count[0].text)
job_data = []

roop_count = int(result_count[0].text[:-1]) // 50 + 1
print(roop_count)
 
for i in range(roop_count):
    d_list = []
    #詳細ボタンの
    elems = driver.find_elements_by_xpath('//*[@id="ID_dispDetailBtn"]')
    for elem in elems:
        d_list.append(elem.get_attribute("href"))
    print(len(d_list))
    for d in d_list:
        res = requests.get(d)
        soup = BeautifulSoup(res.text, "html.parser")
        ukttime = soup.find('div',attrs={'id':'ID_uktkYmd'}).text #受付年月日
        job = soup.find('div',attrs={'id':'ID_sksu'}).text #職種
        sangyo = soup.find('div',attrs={'id':'ID_sngBrui'}).text # 職業分類
        try:
            company_name = soup.find('div',attrs={'id':'ID_jgshMei'}).text #事業者名(非公開の場合もあるのでその場合は例外処理)
            address = soup.find('div',attrs={'id':'ID_szci'}).text # 所在地
        except:
            company_name = '非公開'
            address = '非公開'
        print(d, time,sangyo,company_name,address)
        job_data.append([d, ukttime,sangyo,company_name,address])
    # 次の50件を表示させる
    driver.find_elements_by_xpath('//*[@id="ID_form_1"]/div[6]/div[3]/ul/li[8]/input')[0].click()
    time.sleep(5)

# データをデータフレームに変換する
df = pd.DataFrame(job_data)
print(df)

# csv出力する場合
# df.to_csv('hellowork.csv')
