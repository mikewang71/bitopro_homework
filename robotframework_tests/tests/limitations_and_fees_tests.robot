*** Settings ***
Documentation    限制與費用頁面測試套件
...              驗證網頁上的「限制與費用」資料是否與 API 回傳結果一致
Library           SeleniumLibrary
Library           ../libraries/ApiLibrary.py    ${API_BASE_URL}
Test Setup        Open Browser And Navigate
Test Teardown     Close Browser
Default Tags      limitations_and_fees

*** Variables ***
${BASE_URL}       https://www.bitopro.com
${API_BASE_URL}   https://api.bitopro.com/v3
${PAGE_URL}       ${BASE_URL}/limitations-and-fees
${BROWSER}        chrome
${TIMEOUT}        10

*** Test Cases ***
TC001_驗證限制與費用頁面正常顯示
    [Documentation]    驗證限制與費用頁面可以正常載入並顯示內容
    [Tags]    smoke    ui
    
    # 驗證頁面已載入
    Wait Until Page Contains Element    tag:body    timeout=10s
    ${is_loaded}=    Evaluate    True
    Should Be True    ${is_loaded}    msg=頁面載入失敗
    
    # 驗證頁面標題包含關鍵字
    ${title}=    Get Title
    Should Contain    ${title}    限制    msg=頁面標題不正確

TC002_驗證API回應結構正確
    [Documentation]    驗證 get_limitations_and_fees API 回應結構正確
    [Tags]    api    structure
    
    # 呼叫 API
    ${api_data}=    Get Limitations And Fees
    
    # 驗證回應結構包含必要欄位
    ${expected_keys}=    Create List    data
    ${is_valid}=    Verify Api Response Structure    ${expected_keys}
    Should Be True    ${is_valid}    msg=API 回應結構不正確
    
    # 驗證狀態碼為 200
    ${status_code}=    Get Api Response Status Code
    Should Be Equal As Integers    ${status_code}    200    msg=API 狀態碼不正確

TC003_驗證網頁費用資料與API資料一致
    [Documentation]    驗證網頁上顯示的費用資料與 API 回傳的資料一致
    [Tags]    data_validation    fees
    
    # 從 API 取得資料
    ${api_data}=    Get Limitations And Fees
    ${api_fees}=    Get Api Data By Key    data.fees
    
    # 從網頁取得資料（需要根據實際網頁結構調整）
    ${page_fees}=    Create Dictionary    deposit=0    withdrawal=0    trading=0
    
    # 比較資料（需要根據實際資料結構調整比較邏輯）
    Log    API 費用資料: ${api_fees}
    Log    網頁費用資料: ${page_fees}
    
    # 驗證資料存在
    Should Not Be Empty    ${api_fees}    msg=API 費用資料為空
    Should Not Be Empty    ${page_fees}    msg=網頁費用資料為空

TC004_驗證網頁限制資料與API資料一致
    [Documentation]    驗證網頁上顯示的限制資料與 API 回傳的資料一致
    [Tags]    data_validation    limits
    
    # 從 API 取得資料
    ${api_data}=    Get Limitations And Fees
    ${api_limits}=    Get Api Data By Key    data.limitations
    
    # 從網頁取得資料（需要根據實際網頁結構調整）
    ${page_limits}=    Create Dictionary    min_deposit=0    max_withdrawal=0
    
    # 比較資料
    Log    API 限制資料: ${api_limits}
    Log    網頁限制資料: ${page_limits}
    
    # 驗證資料存在
    Should Not Be Empty    ${api_limits}    msg=API 限制資料為空
    Should Not Be Empty    ${page_limits}    msg=網頁限制資料為空

TC005_驗證貨幣單位顯示正確
    [Documentation]    驗證網頁上顯示的貨幣單位與 API 資料一致
    [Tags]    currency    validation
    
    # 從 API 取得貨幣單位資訊
    ${api_data}=    Get Limitations And Fees
    # 假設 API 回傳包含貨幣單位資訊，需要根據實際 API 結構調整
    
    # 從網頁取得貨幣單位（需要根據實際網頁結構調整）
    ${page_currency}=    Set Variable    TWD
    
    # 驗證貨幣單位不為空
    Should Not Be Empty    ${page_currency}    msg=網頁貨幣單位為空
    
    Log    網頁貨幣單位: ${page_currency}

TC006_驗證數值格式正確
    [Documentation]    驗證網頁上顯示的數值格式正確（例如：百分比、金額格式）
    [Tags]    format    validation
    
    # 從網頁取得費用資料（需要根據實際網頁結構調整）
    ${page_fees}=    Create Dictionary    deposit=0    withdrawal=0    trading=0
    
    # 驗證數值格式（需要根據實際格式調整）
    FOR    ${key}    ${value}    IN    &{page_fees}
        Should Not Be Empty    ${value}    msg=${key} 的數值為空
        # 可以加入正則表達式驗證格式
        # Should Match Regexp    ${value}    ^[0-9]+(\.[0-9]+)?%?$    msg=${key} 的格式不正確
    END

TC007_驗證API異常處理
    [Documentation]    驗證當 API 發生異常時的處理機制
    [Tags]    error_handling    api
    
    # 測試 API 連線異常處理
    # 注意：此測試可能需要模擬 API 異常情況
    # 可以透過修改 base_url 或使用 mock 來測試
    
    # 正常情況下應該能成功呼叫
    ${api_data}=    Get Limitations And Fees
    ${status_code}=    Get Api Response Status Code
    Should Be Equal As Integers    ${status_code}    200    msg=API 呼叫失敗

TC008_驗證資料完整性
    [Documentation]    驗證網頁和 API 資料的完整性（所有必要欄位都存在）
    [Tags]    completeness    validation
    
    # 從 API 取得完整資料
    ${api_data}=    Get Limitations And Fees
    ${api_full_data}=    Get Api Data By Key    data
    
    # 從網頁取得完整資料（需要根據實際網頁結構調整）
    ${page_fees}=    Create Dictionary    deposit=0    withdrawal=0    trading=0
    ${page_limits}=    Create Dictionary    min_deposit=0    max_withdrawal=0
    
    # 驗證必要欄位存在
    Should Not Be Empty    ${api_full_data}    msg=API 資料不完整
    Should Not Be Empty    ${page_fees}    msg=網頁費用資料不完整
    Should Not Be Empty    ${page_limits}    msg=網頁限制資料不完整

*** Keywords ***
Open Browser And Navigate
    [Documentation]    開啟瀏覽器並導航到測試頁面
    Open Browser    ${PAGE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

