*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}    chrome
${URL}    https://hotel.testplanisphere.dev/ja/index.html

*** Keywords ***
画面を起動する
    Open Browser    ${URL}    ${BROWSER}

ログインリンクを押下
    Click Link    link=ログイン

画面を閉じる
    Close Browser