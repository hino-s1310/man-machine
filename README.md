# man-machine

Robot Frameworkのテスト実行結果をStreamlitで可視化するプロジェクト

## 🎯 プロジェクト概要

man-machineは、Robot Frameworkを使用したWebテスト自動化と、その結果をStreamlitで可視化する統合的なテスト管理システムです。テストエンジニアが効率的にテストケースを作成・実行・分析できるWebベースのダッシュボードを提供します。

## ✨ できること

### 🚀 テスト実行管理
- **テストケース作成**: ブラウザベースのGUIでRobot Frameworkテストケースを作成
- **テスト実行**: 選択したテストケースをワンクリックで実行
- **ブラウザ対応**: Chrome、Firefoxでのテスト実行に対応
- **実行オプション**: ログ出力、レポート生成、XML出力、タイムスタンプ付与の設定

### 📊 テスト結果可視化
- **全体サマリー**: 全テストの実行結果を円グラフと棒グラフで表示
- **個別テスト詳細**: 各テストケースの実行結果と信頼性分析
- **実行時間分析**: テスト実行時間の推移をグラフで表示
- **結果ダウンロード**: 実行結果をZIPファイルでダウンロード

### 🔧 テスト自動化
- **Selenium操作**: 画面起動、クリック、入力、値検証、画面閉じるの基本操作
- **ページオブジェクト**: 共通操作とページ固有の操作を分離
- **テストリソース**: 再利用可能なテストキーワードの管理

### 📈 データ分析
- **XML解析**: Robot Frameworkの出力XMLからテスト結果を抽出
- **統計情報**: Pass/Fail/Skip件数の集計と分析
- **信頼性評価**: テストの安定性を数値で評価

## 🏗️ アーキテクチャ

```
man-machine/
├── reports/                 # Streamlitアプリケーション
│   ├── Execution.py        # テスト実行・管理画面
│   ├── pages/
│   │   └── Dashboard.py    # テスト結果可視化ダッシュボード
│   └── data/               # テスト結果データ
│       ├── xml/            # Robot Framework XML出力
│       ├── report/         # HTMLレポート
│       ├── log/            # 実行ログ
│       └── zip/            # 結果ZIPファイル
└── robots/                 # Robot Frameworkテスト
    ├── tests/              # テストケース
    └── pages/              # ページオブジェクト・リソース
```

## 🚀 セットアップ

### 方法1: Docker（推奨）

#### 前提条件
- Docker
- Docker Compose

#### 起動方法
```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# ログ確認
docker-compose logs -f
```

#### アクセス
起動後、ブラウザで http://localhost:8501 にアクセスしてください。

### 方法2: ローカル環境

#### 前提条件
- Python 3.8以上
- Chrome/Firefoxブラウザ
- ChromeDriver/GeckoDriver

#### インストール
```bash
# 依存関係のインストール
pip install -r requirements.txt

# Streamlitアプリケーションの起動
cd reports
streamlit run Execution.py
```

## 📱 使用方法

### 1. テストケース作成
1. 「テスト新規作成」ボタンをクリック
2. ファイル名とテスト概要を入力
3. 実行ブラウザを選択
4. テスト手順を追加（画面起動、クリック、入力、検証、画面閉じる）
5. 「テストを作成する」で.robotファイルを生成

### 2. テスト実行
1. 実行するテストを選択
2. 出力オプションを設定（ログ、レポート、XML、タイムスタンプ）
3. 「Run」ボタンでテスト実行

### 3. 結果確認
1. 「Results」タブで実行結果を確認
2. 「Dashboard」で詳細な分析結果を表示
3. 必要に応じて結果をZIPファイルでダウンロード

## 🔍 現在のテストケース

- **login.robot**: 既存会員ログインテスト
- **open_hotel_top.robot**: トップページ表示テスト
- **open_signup.robot**: サインアップページ表示テスト

## 🗺️ 今後のロードマップ

### Phase 1: 分析機能のリファクタリング・拡充
- [ ] 可視化ダッシュボードの不具合修正
- [ ] 可視化ダッシュボードのリファクタリング
- [ ] メトリクスの拡充

### Phase 2: CI/CD統合
- [ ] GitHub Actions連携
- [ ] Jenkins連携
- [ ] Slack/Teams通知連携
- [ ] テスト結果の自動レポート配信

### Phase 4: テストカバレッジ拡大
- [ ] テストケースの拡充

## 🐳 Docker関連

### コンテナ管理
```bash
# ログ確認
docker-compose logs -f

# コンテナ再起動
docker-compose restart

# 完全クリーンアップ
docker-compose down --rmi all --volumes
```

### データ永続化
- `./reports/data/`: テスト結果データ
- `./robots/`: テストケースファイル
- `./logs/`: アプリケーションログ

---

**man-machine** - テスト自動化と可視化プロジェクト
