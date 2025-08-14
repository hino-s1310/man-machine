*** Settings ***
Library    SeleniumLibrary
Resource    ../pages/common.robot
Resource    ../pages/login_page.robot
Resource    ../pages/my_page.robot

*** Test Cases ***
HOTEL PLANISPHERで既存会員のアカウントでログインする
    画面を起動する
    ログインリンクを押下
    ログイン画面に遷移
    ログイン情報を入力し、ログインボタンを押下
    マイページ画面に遷移
    画面を閉じる


