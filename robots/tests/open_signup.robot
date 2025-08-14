*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
HOTEL PLANISPHEREの会員登録を押下する
    Open Browser    https://hotel.testplanisphere.dev/ja/index.html    chrome
    Click Element    link:会員登録
    Element Should Contain    tag=h2    会員登録
    Close Browser
