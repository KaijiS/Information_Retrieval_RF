# Information_Retrieval_RF

#### ベクトル空間法に基づく情報検索システムの実装演習(適合フィードバック実装)


### 1. 使用した技術要素
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

　
### 2. 動作確認
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
pip(or pip3) install django-bootstrap-form
```
**ライブラリの設定**  
ターミナルなどのコマンドラインにて"Python3"と入力し対話モードへ  
以下の内容を打ち込む
```python:setup
import nltk
nltk.downloads('stopwords')
exit()
```

**開発用サーバの起動**  
`python(or python3) manage.py runserver`   
アクセス先：http://127.0.0.1:8000/search/index/

　
### 3. 全体の設計・構成
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
* 英語論文及び英語技術記事検索(日本語ではないのでMeCabなどによる形態素解析は行わない)
* 検索結果より論文の内容(アブストラクト)の表示
* 適合フィードバックによる検索結果更新  

　
### 4. 使用方法
図1から図5は本webアプリケーションの使用法を順に示している。  
　図1は何も出力されていない状態であるトップページである。検索ワードを入力し、”検索”ボタンをクリックすることで検索を開始する。

　
![top](./explain_image/1-1.png)  
　

　図2は検索結果を表示している画面である。上部にあるヘッダー(①)をクリックするとトップページに遷移する。検索結果の各タイトル(②)をクリックするとその文書の内容を表示する画面(図3)へと遷移する。また、検索によって表示された各文書に対して、適合していると評価した文書についてはタイトルの右部のチェックボックス(③)にチェックを入れる。  

　
![top](./explain_image/2-1.png)  
　

　図3は図2の画面状態にてタイトルをクリックした際、その内容を表示する画面の例である。  

　
![top](./explain_image/3-1.png)  
　

　図4は適合フィードバックを適用する際のボタンを表している。これはチェックボックスのチェック情報に基づいて適合フィードバックを開始する。

　
![top](./explain_image/4-1.png)  
　

　図5は適合フィードバックを適用した際の結果例を表している。この結果に対して更に繰り返し適合フィードバックを適用することもできる。  

　
![top](./explain_image/5-1.png)  
　
　

#### 使用させて頂いた論文及び記事
1. A.Costa et al, Efficient Parameter Estimation for Information Retrieval using Black-box Optimization, 2017
2. I.Zeroual et al, Arabic information retrieval: Stemming or lemmatization?, 2017
3. A.Goker et al, Performance Issues in Parallel Computing for Information Retrieval, 2009
4. A.Goker et al, Context and Information Retrieval, 2009
5. A.Goker et al, The Role of Natural Language Processing in Information Retrieval: Searching for Meaning and Structure, 2009
6. A.Khan et al, Vision Based Information Retrieval, 2017
7. A.Goker et al, Information Retrieval Models, 2009
8. A.Goker et al, Web Information Retrieval, 2009
9. A.Goker et al, User‐Centred Evaluation of Information Retrieval Systems, 2009
10. A.Goker et al, Cross‐Language Information Retrieval, 2009
11. H.Cho et al, Information Needs for Anime Recommendation: Analyzing Anime Users' Online Forum Queries, 2017
12. Q.Zhao et al, A Novel Method on Information Recommendation via Hybrid Similarity, 2016
13. C.Li et al, The design of employment information recommendation system, 2016
14. B.He et al, Library personalized information recommendation of big data, 2016
15. H.Haiyan et al, Design and Implementation of Agricultural Production and Market Information Recommendation System Based on Cloud Computing, 2016
16. Haiyan Hu et al, A Study on Key Techniques of Wisdom Campus Information Recommendation Platform Based on Big Data, 2015
17. X.Zhou et al, Social Stream Organization Based on User Role Analysis for Participatory Information Recommendation, 2014
18. J.Oliveira et al, Collaborative information gathering and recommendation using mobile computing, 2013
19. X.Han et al, A Big Data Model Supporting Information Recommendation in Social Networks, 2012
20. K.Christidis et al, A socially intelligent approach for enterprise information search and recommendation, 2012
