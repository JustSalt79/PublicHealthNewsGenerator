# 公共衛生新聞生成器教程

本教程將介紹如何使用Python建立一個公共衛生新聞生成器。這個應用程式使用Streamlit建立用戶界面，結合PubMed和Google Scholar搜索功能，並利用OpenAI的GPT模型生成新聞內容。

## 1. 導入必要的庫

首先，我們需要導入所有必要的Python庫：

```python
import streamlit as st
from googletrans import Translator
import openai
import requests
from bs4 import BeautifulSoup
import re
```

這些庫包括：
- Streamlit：用於創建Web應用界面
- Googletrans：用於翻譯文本
- OpenAI：用於使用GPT模型生成內容
- Requests：用於發送HTTP請求
- BeautifulSoup：用於解析HTML和XML
- re：用於正則表達式操作

## 2. 設置OpenAI API金鑰

為了使用OpenAI的服務，我們需要設置API金鑰：

```python
openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]
```

這裡使用了Streamlit的secrets功能來安全地存儲API金鑰。

## 3. 定義PubMed搜索功能

接下來，我們定義了一個函數來搜索PubMed數據庫：

```python
def search_pubmed(query, num_results=10):
    # ... [函數內容]
```

這個函數使用PubMed的API來搜索文章，並返回包含標題、摘要、作者、期刊和URL的結果列表。

## 4. 定義Google Scholar搜索功能

類似地，我們定義了一個函數來搜索Google Scholar：

```python
def search_google_scholar(query, num_results=10):
    # ... [函數內容]
```

這個函數使用網頁抓取技術來獲取Google Scholar的搜索結果，返回標題、摘要、作者、期刊和URL信息。

## 5. 定義內容生成功能

這個函數使用OpenAI的GPT模型來生成新聞內容：

```python
def generate_content_with_references(prompt, topic, references):
    # ... [函數內容]
```

它接受一個提示、主題和參考資料列表，然後使用GPT模型生成包含參考文獻的內容。

## 6. 創建Streamlit應用界面

現在，我們開始創建Streamlit應用的用戶界面：

```python
st.title('🩺📰 Public Health News Generator')
topic = st.text_input('News topic: ')
```

這裡創建了一個標題和一個輸入框，讓用戶輸入新聞主題。

## 7. 翻譯用戶輸入

為了確保能夠處理不同語言的輸入，我們將用戶輸入翻譯成英文：

```python
translator = Translator()
if topic:
    topic_en = translator.translate(topic, src='auto', dest='en').text
else:
    st.error('Please enter a news topic.')
    st.stop()
```

## 8. 生成新聞內容

當用戶輸入主題後，我們開始生成新聞內容：

```python
if topic:
    with st.spinner('Generating evidence-based article...'):
        # ... [生成內容的代碼]
```

這個過程包括：
1. 搜索PubMed和Google Scholar獲取參考資料
2. 為每個新聞部分（介紹、流行病學、原因、預防、護理和治療）生成內容
3. 將所有部分組合成一篇完整的文章
4. 為文章生成標題

## 9. 翻譯和顯示結果

最後，我們將生成的英文內容翻譯成繁體中文，並顯示結果：

```python
translator = Translator()
translated_title = translator.translate(title, src='en', dest='zh-tw').text
translated_article = translator.translate(article, src='en', dest='zh-tw').text

st.subheader(translated_title)
st.write(translated_article)

with st.expander('Original English Content'):
    st.subheader(title)
    st.write(article)
```

這樣，用戶就可以看到生成的中文新聞內容，同時也可以查看原始的英文版本。

通過以上步驟，我們創建了一個能夠根據用戶輸入的主題，自動生成基於科學證據的公共衛生新聞的應用程式。
