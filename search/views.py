from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from search.models import Paper

import nltk
from nltk.corpus import stopwords
import numpy as np
import math
import re


def prepro(document):
    """文書前処理"""
    tmp = document.replace('.', '').replace(',', '').replace('\"', '').replace('\'', '').replace('¥n', '') #句読点や改行などを削除
    tmp = re.sub(re.compile("[!-/:-@[-`{-~]"), '', tmp) #半角記号を削除
    tmp = tmp.split(" ") # スペースを区切りにリスト化
    return tmp


def removeStoplist(document):
  """ストップワードを取り除く"""
  stoplist_removed_document = []
  for word in document:
      if word not in stopwords.words('english'):
        stoplist_removed_document.append(word)
  return stoplist_removed_document


def stemming(document):
    """ステミング処理"""
    stemmer = nltk.PorterStemmer()
    stem = []
    for word in document:
        stem.append(stemmer.stem(word))
    return stem


def make_term(documents):
    """全文書による単語リストを作成"""
    all_term=[]
    for i in documents:
        for j in i:
            if j not in all_term:
                all_term.append(j)
    return(all_term)


def tf(terms, document):
    """任意の文書のTF値の計算"""
    tf_values = [document.count(term) for term in terms]
    return list(map(lambda x: math.log10(x+1)/math.log10(sum(tf_values)), tf_values))


def idf(terms, documents):
    """任意の文書のIDF値の計算"""
    return list(map(lambda x : x+1, [math.log10(len(documents)/sum([bool(term in document) for document in documents])) for term in terms]))


def tf_idf(terms, documents):
    """文章毎にTF-IDF値を計算"""
    return [[_tf*_idf for _tf, _idf in zip(tf(terms, document), idf(terms, documents))] for document in documents]


def cos_sim(x,y):
    """コサイン類似度の計算"""
    if np.linalg.norm(x)==0 or np.linalg.norm(y)==0:
        return 0
    else:
        return np.dot(x,y) / (np.linalg.norm(x) * np.linalg.norm(y))


# 行に文書,列に単語のリストを作成
doc = []
# for i in range(20): # file_number
for i in Paper.objects.all():
    tmp = stemming(removeStoplist(prepro(i.abst)))
    doc.append(tmp)

#全出現単語
all_terms = make_term(doc)

# tf-idfを計算しファイルに出力(行に各文書ベクトル、列はベクトルの各次元の要素)
doc_vec = tf_idf(make_term(doc),doc)


def Index(request):
    """検索結果"""
    query_flag = 0
    query_vec = None
    first_query = 1
    query_list = None

    if request.method == 'GET' :
        query = request.GET.get('query') #検索ワード：query

        #キーワードが入力された時
        if query:
            query_list = query.split(" ") # スペースを区切りにリスト化
            query_tmp = stemming(removeStoplist(prepro(query)))

            # クエリのベクトル生成
            query_vec = np.zeros(len(all_terms))
            for i in query_tmp:
                if i in all_terms:
                    query_vec[all_terms.index(i)] = 1

            #フラグ処理
            query_flag = 1
            first_query = 0


    # リランキングをしたとき
    if request.method == 'POST':

        #ここからしばらく都合よく処理
        beta_list = request.POST.getlist('beta')
        for i in range(len(beta_list)):
            beta_list[i] = int(beta_list[i])

        query_list = request.POST.getlist('query')
        query = ' '.join(query_list)
        query_vec = request.POST.getlist('query_vec')
        for i in range(len(query_vec)):
            query_vec[i] = float(query_vec[i])
        query_vec = np.array(query_vec)

        #適合フィードバックの計算開始
        beta_count = 0
        sum_beta_vec = np.zeros(len(all_terms))
        gamma_count = 0
        sum_gamma_vec = np.zeros(len(all_terms))
        for i in Paper.objects.all():
            if i.id in beta_list:
                beta_count += 1
                sum_beta_vec += doc_vec[int(i.id)-1]
            else:
                gamma_count += 1
                sum_gamma_vec += doc_vec[int(i.id)-1]

        alpha = 8
        beta =  16
        gamma = 4
        query_vec = alpha * query_vec + beta * sum_beta_vec / beta_count - gamma * sum_gamma_vec / gamma_count #Rocchioの式

        #フラグ処理
        query_flag = 1
        first_query = 0


    result_title = []
    result_abst = []
    len_abst = []
    p_id = []
    search_flag = '0'

    if query_flag == 1:

        # クエリベクトルと各文書ベクトルとのコサイン類似度を算出し、
        # 文書ベクトルと対応するリストの位置に類似度の値を代入
        sim_array = np.zeros(len(doc_vec))
        for i in range(len(doc_vec)):
            sim_array[i] = cos_sim(query_vec,doc_vec[i])

        # 検索ワードとの類似度が高い順にソート(ランキング化)し、その元のindexをリスト化
        dec_doc=[]
        for i in range(len(sim_array)):
            # print(np.sort(sim_array)[::-1][i])  # 類似度を出力
            if np.sort(sim_array)[::-1][i] > 0:
                dec_doc += [np.argsort(sim_array)[::-1][i]]

        # ランキングが高い順にリストに追加
        for i in dec_doc:
             for j in Paper.objects.all():
                 if (i+1) == j.id:
                     result_title += [j.title]
                     result_abst += [j.abst[:200]]
                     len_abst += [len(j.abst)]
                     p_id += [str(j.id)]

        #フラグ処理
        search_flag = '1'

    d = {
        'query':query,
        'query_list':query_list,
        'query_vec':query_vec,
        'search_flag':search_flag,
        'result_title':result_title,
        'result_abst':result_abst,
        'len_abst':len_abst,
        'p_id':p_id,
        'result_num':str(len(result_abst)),
        'first_query':first_query,
    }
    return render(request, 'search/index.html',d)


def Content(request,paper_id):
    """コンテンツ表示"""

    cont = get_object_or_404(Paper, pk=paper_id)
    contexts = {
        'title':cont.title,
        'abst':cont.abst,
    }
    return render(request,'search/content.html',contexts)
