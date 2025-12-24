*** Settings ***
Documentation    全域設定檔
...              包含共用的設定和變數
Library           SeleniumLibrary
Library           libraries/ApiLibrary.py    ${API_BASE_URL}
Library           pages/LimitationsAndFeesPage.py

*** Variables ***
${API_BASE_URL}   https://api.bitopro.com/v3
${WEB_BASE_URL}   https://www.bitopro.com
${BROWSER}        chrome
${TIMEOUT}        10

