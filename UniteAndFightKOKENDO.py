# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 19:21:19 2019

@author: 
"""

from selenium import webdriver
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

#chrome起動
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=**ChromeFileDir**") #Path to your chrome profile
#options.set_headless(True)
driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)

#古戦場ページへ遷移(古戦場ごとに変更の必要あり最後の数字が第XXX回）
driver.get("http://game.granbluefantasy.jp/#event/teamraid042")
sleep(3)

#貢献度取得
guildPoint = driver.find_element_by_class_name("txt-guild-point").text
rivalPoint = driver.find_element_by_class_name("txt-rival-point").text

#直近1時間のログイン人数取得（現在のところ相手団のみ）
rivalAirshipURL = driver.find_element_by_class_name("btn-rival-airship").get_attribute('data-href')

#相手団ページへ遷移
driver.get("http://game.granbluefantasy.jp/#" + rivalAirshipURL)
sleep(3)

#相手団の直近1時間のログイン人数を取得
elements = driver.find_elements_by_class_name("prt-status-value")
for element in elements:
    rivalLoginMem = element.text

#ブラウザを閉じる
driver.close()

##以下スプレッドシート関連
#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('*******************.json', scope)
#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '*SPREADSHEET_KEY*'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

#F2セルの値を受け取る
import_value = int(worksheet.acell('F2').value)

#spreadsheetへの書き込み
worksheet.update_cell(import_value,2,guildPoint)
worksheet.update_cell(import_value,3,rivalPoint)
worksheet.update_cell(import_value,4,rivalLoginMem)

import_value += 1
#最後の処理
if import_value == 43:
    worksheet.update_cell(2,6,10)
#次への準備
else:
    worksheet.update_cell(2,6,import_value)

    
    








