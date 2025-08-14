# Contributing to man-machine

man-machineプロジェクトへのコントリビューションをありがとうございます！このドキュメントでは、プロジェクトの開発に参加するためのルールとガイドラインを説明します。

## 🌿 ブランチルール

### ブランチ命名規則

#### メインブランチ
- `main` - 本番環境用の安定版ブランチ
- `develop` - 開発用の統合ブランチ

#### 作業ブランチ
- `feature/機能名` - 新機能開発
  - 例: `feature/database-integration`
  - 例: `feature/cloud-deployment`
- `fix/修正内容` - バグ修正
  - 例: `fix/dashboard-error`
  - 例: `fix/test-execution-failure`
- `refactor/リファクタリング内容` - コードリファクタリング
  - 例: `refactor/dashboard-components`
  - 例: `refactor/database-queries`
- `docs/ドキュメント内容` - ドキュメント更新
  - 例: `docs/api-documentation`
  - 例: `docs/user-guide`

### ブランチ作成・管理ルール

1. **作業開始時**
   ```bash
   # developブランチから最新を取得
   git checkout develop
   git pull origin develop
   
   # 新しい作業ブランチを作成
   git checkout -b feature/your-feature-name
   ```

2. **作業完了時**
   ```bash
   # 作業ブランチをプッシュ
   git push origin feature/your-feature-name
   
   # プルリクエストを作成（developブランチ向け）
   ```

3. **緊急修正時**
   ```bash
   # mainブランチから直接作成
   git checkout main
   git pull origin main
   git checkout -b hotfix/urgent-fix
   ```

### ブランチ保護ルール

- `main`ブランチ: 直接プッシュ禁止、プルリクエスト必須
- `develop`ブランチ: 直接プッシュ禁止、プルリクエスト必須
- 作業ブランチ: 開発者による直接プッシュ可能

## 📝 コミットルール

### コミットメッセージ形式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type（必須）
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: バグ修正や機能追加ではないコードの変更
- `perf`: パフォーマンスを改善するコードの変更
- `test`: テストの追加や修正(e2eテストの実装も含む）
- `chore`: ビルドプロセスや補助ツールの変更

#### Scope（オプション）
- `ui`: ユーザーインターフェース関連
- `api`: API関連
- `db`: データベース関連
- `test`: テスト関連
- `docker`: Docker関連
- `ci`: CI/CD関連

#### Subject（必須）
- 50文字以内
- 現在形で記述
- 文末にピリオドなし
- 命令形で記述

#### Body（オプション）
- 変更の理由や詳細を記述
- 72文字以内で改行

#### Footer（オプション）
- 破壊的変更の説明
- 関連するIssue番号

### コミットメッセージ例

#### 新機能追加
```
feat(ui): テスト結果のグラフ表示機能を追加

- 円グラフでPass/Fail/Skipの割合を表示
- 棒グラフで実行時間の推移を表示
- Plotlyライブラリを使用したインタラクティブなグラフ

Closes #123
```

#### バグ修正
```
fix(test): テスト実行時のタイムアウトエラーを修正

- 長時間実行されるテストのタイムアウト設定を調整
- エラーハンドリングを改善

Fixes #456
```

#### ドキュメント更新
```
docs: READMEにDocker起動方法を追加

- Docker Composeでの起動手順を記載
- 環境構築の手順を簡素化
```

#### リファクタリング
```
refactor(db): データベースクエリの最適化

- N+1問題を解決するためのクエリ改善
- インデックスの追加によるパフォーマンス向上
```

### コミットルール

1. **1つのコミット = 1つの変更**
   - 複数の機能や修正を1つのコミットにまとめない
   - 関連する変更は別々のコミットに分ける

2. **コミット前の確認**
   ```bash
   # 変更内容を確認
   git status
   git diff --staged
   
   # コミット
   git commit -m "type(scope): subject"
   ```

3. **コミット履歴の整理**
   ```bash
   # 複数のコミットを1つにまとめる
   git rebase -i HEAD~3
   
   # コミットメッセージの修正
   git commit --amend
   ```

## 🔄 プルリクエストルール

### プルリクエスト作成時

1. **タイトル**
   - コミットメッセージと同様の形式
   - 例: `feat(ui): テスト結果のグラフ表示機能を追加`

2. **説明**
   - 変更内容の詳細
   - 変更理由
   - テスト方法
   - 関連するIssue番号

3. **ラベル**
   - `enhancement`: 新機能
   - `bug`: バグ修正
   - `documentation`: ドキュメント
   - `refactoring`: リファクタリング

## 🚀 開発環境のセットアップ

### 必要なツール

- Git 2.30以上
- Python 3.8以上
- Docker & Docker Compose
- コードエディタ（VSCode推奨）

### 初期設定

```bash
# リポジトリをクローン
git clone https://github.com/your-username/man-machine.git
cd man-machine

# 開発ブランチを作成
git checkout -b develop

# 依存関係をインストール
pip install -r requirements.txt

# Docker環境を起動
docker-compose up -d
```

**man-machine** - テスト自動化と可視化プロジェクト
