import streamlit as st
from streamlit.column_config import Column
import subprocess as sb
import pandas as pd
import os, glob
from xmltodict import parse
import zipfile
import uuid

st.set_page_config(page_title="man-machine", layout="wide")

# タブの作成
tab_exec, tab_results= st.tabs(["Execution", "Results"])

with tab_exec:

    browsers = ['chrome', 'Firefox']
    keywords = ["画面を起動する","クリックする","入力する","値を検証する","画面を閉じる"]


    @st.dialog("新しくテストを作成する", width="large")
    def add_new_test():
        st.header("テストケースの作成")
        # ファイル名入力
        test_file_name = st.text_input("ファイル名",placeholder="sample")

        # ファイルに書き込むリストの定義
        rf_lines = ["*** Settings ***\nLibrary    SeleniumLibrary\n", "\n", "*** Test Cases ***\n"]

        # テストの概要を入力する
        test_summary = st.text_input("テストの概要", placeholder="新規会員登録")
        rf_lines.append(test_summary+"\n")

        # 実行ブラウザを選択してください
        browser = st.selectbox("テストするブラウザ",
                                    browsers,
                                    index=0
                                )

        # テスト手順作成
        # １行目
        process_flag = False

        if "unique_id1" not in st.session_state and "unique_id2" not in st.session_state and "unique_id3" not in st.session_state:
            st.session_state["unique_id1"] = []
            st.session_state["unique_id2"] = []
            st.session_state["unique_id3"] = []
            st.session_state["unique_id4"] = []


        add_process, pop_process = st.columns([3,1], gap="small")
        
        with add_process:
            if st.button("手順の追加", use_container_width=True):
                st.session_state["unique_id1"].append(uuid.uuid1())
                st.session_state["unique_id2"].append(uuid.uuid1())
                st.session_state["unique_id3"].append(uuid.uuid1())
                st.session_state["unique_id4"].append(uuid.uuid1())


        with pop_process:
            if st.button("手順の削除", use_container_width=True , disabled=process_flag):
                st.session_state["unique_id1"].pop(-1)
                st.session_state["unique_id2"].pop(-1)
                st.session_state["unique_id3"].pop(-1)
                st.session_state["unique_id4"].pop(-1)
        
        for (unique_id1,unique_id2,unique_id3,unique_id4) in zip(st.session_state["unique_id1"],st.session_state["unique_id2"],st.session_state["unique_id3"],st.session_state["unique_id4"]):

            with st.container():
                keyword, url, locator, value = st.columns([2,2,1,1])

                # 入力の活性状態を制御するフラグ
                flag_disabled_url = False
                flag_disabled_locator = False
                flag_disabled_value = False

                # テスト手順の初期化
                rf_keyword = ""
                rf_url = ""
                rf_locator = ""
                rf_value = ""


                with keyword:
                    rf_keyword_default = st.selectbox("アクション選択",
                                            keywords,
                                            index=0,
                                            key=unique_id1)
                    match rf_keyword_default:
                        case rf_keyword_default if rf_keyword_default == keywords[0]:
                            rf_keyword = "    Open Browser"
                            flag_disabled_locator = True
                            flag_disabled_value = True

                        case rf_keyword_default if rf_keyword_default == keywords[1]:
                            rf_keyword = "    Click Element"
                            flag_disabled_url = True
                            flag_disabled_value = True

                        case rf_keyword_default if rf_keyword_default == keywords[2]:
                            rf_keyword = "    Input Text"
                            flag_disabled_url = True

                        case rf_keyword_default if rf_keyword_default == keywords[3]:
                            rf_keyword = "    Element Should Contain"
                            flag_disabled_url = True

                        case rf_keyword_default if rf_keyword_default == keywords[4]:
                            rf_keyword = "    Close Browser"
                            flag_disabled_url = True
                            flag_disabled_locator = True
                            flag_disabled_value = True
                
                with url:
                    if not flag_disabled_url:
                        rf_url = "    " + st.text_input("URL入力", placeholder="https://~",key=unique_id2, disabled=flag_disabled_url) + f"    {browser}"

                with locator:
                    if not flag_disabled_locator:
                        rf_locator = "    " + st.text_input("ロケータ入力", placeholder="link=XXX",key=unique_id3, disabled=flag_disabled_locator)

                with value:
                    if not flag_disabled_value:
                        rf_value = "    " + st.text_input("値入力", placeholder="ログイン",key=unique_id4, disabled=flag_disabled_value)

                rf_lines.append(f"{rf_keyword}{rf_url}{rf_locator}{rf_value}\n")

        # フッター部分の処理
        if st.button('テストを作成する', type="primary", use_container_width=True, disabled=process_flag):
            st.session_state.new_test = {'rf_keyword': rf_keyword}
            # .robotファイルを作成する
            path = f'../robots/tests/{test_file_name}.robot'
            f = open(path, 'w')
            for i in range(len(rf_lines)):
                f.write(rf_lines[i]) 
            st.rerun()
            f.close()            
        
    with st.container():
        title, button = st.columns([5,1])
        
        with title:
            st.title("Test Execution")

        with button:
            if 'new_test' not in st.session_state:
                if st.button("テスト新規作成"):
                    add_new_test()
            else:
                if st.button("テスト新規作成"):
                    add_new_test()

    # testsフォルダからテスト一覧を取得
    dir_path = "../robots/tests"
    tests = os.listdir(dir_path)

    # 実行するテストを選択
    test = st.selectbox(
        '実行テスト一覧',
        tests
    )

    #ファイル名の拡張子以外を出力
    test_no_extension = os.path.splitext(test)[0]

    # サブプロセスの実行コマンドとオプションを格納するリストを定義
    exec_command = ["robot"]

    # 追加するオプションを変数定義
    log_option = "--log"
    log_path = f"data/log/{test_no_extension}.html"

    report_option = "--report"
    report_path = f"data/report/{test_no_extension}.html" 

    xml_option = "--output"
    xml_path = f"data/xml/{test_no_extension}.xml"

    timestamp_option = "--timestampoutputs"

    file_path = "../robots/tests/" + test

    with st.expander("実行オプション"):

        # ログ出力に関する処理
        exec_command.append(log_option)
        check_log = st.checkbox("ログを出力する", value=True)
        if check_log:
            exec_command.append(log_path)
        else:
            exec_command.append("None")

        # レポート出力の引数を追加する処理
        exec_command.append(report_option)
        check_report = st.checkbox("実行レポートを出力する", value=True)
        if check_report:
            exec_command.append(report_path)
        else:
            exec_command.append("None")

        # XML出力の引数を追加する処理
        exec_command.append(xml_option)
        check_xml = st.checkbox("XMLファイルを出力する", value=True)
        if check_xml:
            exec_command.append(xml_path)
        else:
            exec_command.append("None")

        check_time_stamp = st.checkbox("タイムスタンプを付ける", value=True)
        if check_time_stamp:
            # タイムスタンプ付与を実行コマンドリストに追加
            exec_command.append(timestamp_option)

    # 実行ファイル名を実行コマンドリストに追加
    exec_command.append(file_path)
    console_log = ""
    if st.button("Run", type="primary"):
        with st.spinner('Wait for it...'):
            console_log = sb.run(exec_command, capture_output=True, text=True).stdout
        st.success("実行が完了しました")

        #コンソールの出力をテキストフィールドに出力
        results_log = st.text_area(label="コンソール出力結果", height=256, value=console_log, disabled=True)

# xmlフォルダから昇順にソートしたxml一覧を取得
xml_path = "data/xml"
test_xml = sorted(os.listdir(xml_path))

test_results = []
test_dates = []

for i in range(len(test_xml)):
    with open(f"../reports/data/xml/{test_xml[i]}") as fd:
        parsed_data = parse(fd.read())

    # 実行結果データを抽出
    stat_data_results = parsed_data["robot"]["statistics"]["total"]["stat"]
    suite_data_dates = parsed_data["robot"]["suite"]["status"]["@start"]

    if stat_data_results["@pass"] == "1":
        test_results.append("✅")
        test_dates.append(suite_data_dates)
        
    elif stat_data_results["@fail"] == "1":
        test_results.append("❌")
        test_dates.append(suite_data_dates)

    elif stat_data_results["@skip"] == "1":
        test_results.append("Skip")
        test_dates.append(suite_data_dates)    

with tab_results:

    # report,logフォルダから昇順にソートしたテスト実行レポートを取得
    report_path = "data/report"
    test_reports = sorted(os.listdir(report_path))

    log_paths = sorted(glob.glob("data/log/*.html"))
    test_logs = []
    for i in range(len(log_paths)):
        test_logs.append(os.path.basename(log_paths[i]))

    st.title("Results")

    results_data = pd.DataFrame({
        "results": test_results,
        "date":test_dates,
        "report": test_reports
    })

    # カスタム列設定
    column_config = {
        "results": Column(
            label="実行結果",
            width=8,
            help="実行結果を表示します"
        ),
        "date": Column(
            label="実行開始日付",
            width=128,
            help="実行開始した時間を表示します",
            required=True
        ),
        "report": Column(
            label="実行結果レポート",
            width=256,
            help="実行結果のレポート名を表示します",
            disabled=False
        )
    }

    st.subheader("テスト実行結果を表示します")
    st.dataframe(results_data, 
                hide_index=True,
                column_config=column_config,
                use_container_width=True)

    # html形式のレポートを描画
    test_report = st.selectbox(
        '確認するレポートを選択してください',
        test_reports
    )

    test_report_no_extension = os.path.splitext(test_report)[0]
    zip_file_path = f"data/zip/{test_report_no_extension}.zip"

    compFile = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
    compFile.write(f"data/xml/{test_report_no_extension}.xml")
    compFile.write(f"data/report/{test_report}")
    compFile.write(f"data/log/{test_report}")
    compFile.close()

    with open(zip_file_path, "rb") as fp:
        btn = st.download_button(
            label="実行結果レポートをダウンロード",
            data=fp,
            file_name=f"{test_report_no_extension}.zip",
            mime="application/zip",
            type="primary"
        )