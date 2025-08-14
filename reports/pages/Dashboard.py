import streamlit as st
from xmltodict import parse
import pandas as pd
import plotly.graph_objects as go
import os, glob

st.set_page_config(page_title="man-machine", layout="wide")
st.title("Test Automation Dashboard")

# タブの作成
tab_whole, tab_individual= st.tabs(["全体サマリ", "各テスト詳細"])

# testsフォルダから昇順にソートしたテスト一覧を取得
dir_path = "../robots/tests"
tests = sorted(os.listdir(dir_path))
tests_no_extension = []

for i in range(len(tests)):
    tests_no_extension.append(os.path.splitext(tests[i])[0])

#実行結果の初期化
pass_amount_whole = 0
fail_amount_whole = 0
skip_amount_whole = 0

# 各タブに内容を追加
with tab_whole:
    st.header("全体サマリー")

    # xmlフォルダからxml一覧を取得
    xml_path_whole = "data/xml"
    test_xml = sorted(glob.glob(f"{xml_path_whole}/*.xml"))

    with st.container():        
        st.subheader("実行結果")

        # xmlデータを辞書型に加工
        for i in range(len(test_xml)):   
            with open(f"../reports/{test_xml[i]}") as fd:
                parsed_data = parse(fd.read())
            
            # 実行結果データを抽出
            stat_data = parsed_data["robot"]["statistics"]["suite"]["stat"]
            pass_amount_whole += int(stat_data["@pass"])
            fail_amount_whole += int(stat_data["@fail"])
            skip_amount_whole += int(stat_data["@skip"])

        # 合計実行回数の算出
        total_amount = pass_amount_whole + fail_amount_whole + skip_amount_whole

        pie_chart, bar_chart = st.columns(2)

        with pie_chart:
            st.write("全テスト結果一覧")
            with st.spinner('Wait for it...'):

                # データフレームに加工
                chart_data = {
                    "実行結果":["Pass","Fail","Skip"],
                    "件数": [pass_amount_whole, fail_amount_whole, skip_amount_whole] 
                }
                df = pd.DataFrame(chart_data)

                # 基本的な円グラフの作成
                fig = go.Figure(data=[go.Pie(labels=df["実行結果"],
                                            values=df["件数"],
                                            hole = .4,
                                            )])
                fig.update_traces(marker=dict(colors=["	#1be300", "#E3001B", "#fafafa"]))
                fig.update_layout(title='実行結果')
                st.plotly_chart(fig)

        with bar_chart:
            st.write("テストごとの結果一覧")

    with st.container():
        st.subheader("実行時間")
        with st.spinner('Wait for it...'):
            test_execution_time = []

            for i in range(len(test_xml)):
                with open(f"../reports/{test_xml[i]}") as fd:
                    parsed_data = parse(fd.read())

                # 実行開始時間、実行時間データを抽出
                test_execution_time.append(float(parsed_data["robot"]["suite"]["status"]["@elapsed"]))

            # 実行時間グラフの作成
            data = pd.DataFrame({
                "name": test_xml,
                "time": test_execution_time
            })
            st.bar_chart(data.set_index("name"), color="#1be300")  

with tab_individual:

    # testsフォルダから昇順にソートしたテスト一覧を取得
    dir_path = "../robots/tests"
    tests = sorted(os.listdir(dir_path))

    # 実行するテストを選択
    test = st.selectbox(
        '実行結果を表示するテストを選択してください',
        tests
    )

    #ファイル名の拡張子以外を出力
    test_no_extension = os.path.splitext(test)[0]

    # xmlフォルダからxml一覧を取得
    xml_path = "data/xml"
    test_xml = sorted(glob.glob(f"{xml_path}/{test_no_extension}-*"))

    #実行結果の初期化
    pass_amount = 0
    fail_amount = 0
    skip_amount = 0

    # xmlデータを辞書型に加工
    for i in range(len(test_xml)):   
        with open(f"../reports/{test_xml[i]}") as fd:
            parsed_data = parse(fd.read())
        
        # 実行結果データを抽出
        stat_data = parsed_data["robot"]["statistics"]["suite"]["stat"]
        pass_amount += int(stat_data["@pass"])
        fail_amount += int(stat_data["@fail"])
        skip_amount += int(stat_data["@skip"])

    total_amount = pass_amount + fail_amount + skip_amount

    with st.container():
        execute_amount, execute_proportion = st.columns(2)
        with execute_amount:
            st.subheader(f"自動テスト実行回数:  {total_amount}回")
            st.write(f"Pass回数: {pass_amount}回")
            st.write(f"Fail回数: {fail_amount}回")
            st.write(f"Skip回数: {skip_amount}回")

            st.subheader("このテストの信頼性")
            if(pass_amount / total_amount > 0.79):
                st.write("テストは安定して動いています。")
            else:
                st.write("この自動テストはFlakyです。")

        with execute_proportion:
            with st.spinner('Wait for it...'):
                st.subheader("自動テスト結果内訳")
                # データフレームに加工
                chart_data = {
                    "実行結果":["Pass","Fail","Skip"],
                    "件数": [pass_amount, fail_amount, skip_amount] 
                }

                df = pd.DataFrame(chart_data)

                # 基本的な円グラフの作成
                fig = go.Figure(data=[go.Pie(labels=df["実行結果"],
                                            values=df["件数"],
                                            hole = .4,
                                            )])
                fig.update_traces(marker=dict(colors=["	#1be300", "#E3001B", "#fafafa"]))
                fig.update_layout(title='実行結果')
                st.plotly_chart(fig)

    st.header("実行時間の推移を表示します")
    with st.spinner('Wait for it...'):
        test_execution_date = []
        test_execution_time = []

        for i in range(len(test_xml)):
            with open(f"../reports/{test_xml[i]}") as fd:
                parsed_data = parse(fd.read())

            # 実行開始時間、実行時間データを抽出
            test_execution_date.append(parsed_data["robot"]["suite"]["status"]["@start"])
            test_execution_time.append(float(parsed_data["robot"]["suite"]["status"]["@elapsed"]))   

        # 実行時間グラフの作成
        data = pd.DataFrame({
            "date": test_execution_date,
            "time": test_execution_time
        })
        st.line_chart(data.set_index("date"), color="#1be300")

