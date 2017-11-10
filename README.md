# Information_Retrieval_RF

### ベクトル空間法に基づく情報検索システムの実装(適合フィードバック実装)


#### 1. 使用した技術要素
言語:Python3  
フレームワーク:Django  
データベース:SQLite(Djangoの初期設定)  

**文書ベクトル作成時**
* ストップワード削除
* ステミング処理
* TF-IDF

**文書間類似度尺度**
* コサイン類似度

**適合フィードバック**
* Rocchioの式

　
#### 2. 動作確認
**確認環境**  
OS: macOS Sierra バージョン 10.12.6  
ブラウザ: Google Chrome  
言語: Python3.6.2  
以下の必要ライブラリ

**必要ライブラリのインストール**
```
pip(or pip3) install django
pip(or pip3) install nltk
pip(or pip3) install numpy
```

**開発用サーバの起動**  
`python(or python3) manage.py runserver`   
アクセス先：http://127.0.0.1:8000/search/index/

　
#### 3. 全体の設計・構成
**ファイル構成**   
Information_Retrieval_RF(プロジェクト名)  
　　|-search(アプリ名)  
　　|　　|--template(HTMLなど表示周り)  
　　|　　|--他(内部の実装)  
　　|  
　　|-search_engine(プロジェクトの設定)  
　　|  
　　|-static(BootstrapやjQuery,背景画像)  

**データベース設計**  
テーブル名:Paper(属性:ID,論文タイトル,論文アブストラクト)  

**機能**
* 論文検索
* 検索結果より論文の内容(アブストラクト)の表示
* 適合フィードバックによる検索結果更新
