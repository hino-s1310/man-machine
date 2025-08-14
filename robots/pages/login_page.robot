*** Settings ***
Library    SeleniumLibrary
Resource    common.robot

*** Variables ***
${email}    ichiro@example.com
${password}    password

*** Keywords ***
ログイン画面に遷移
    Wait Until Element Is Visible    tag=h2
    Element Should Contain    tag=h2    ログイン

ログイン情報を入力し、ログインボタンを押下
    Input Text    id=email    ${email}
    Input Password    id=password    ${password}
    Click Button    id=login-button
