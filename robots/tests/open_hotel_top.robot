*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
HOTEL PLANISPHEREのトップページを起動する
    Open Browser    https://hotel.testplanisphere.dev/ja/index.html    chrome
    Element Should Contain    tag=h1    HOTEL PLANISPHERE
    Close Browser
