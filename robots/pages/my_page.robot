*** Settings ***
Library    SeleniumLibrary
Resource    common.robot

*** Keywords ***
マイページ画面に遷移
    Wait Until Element Is Visible    tag=h2
    Element Should Contain    tag=h2    マイページ