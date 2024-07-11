# 公共衛生新聞產生器教程

本教程將介紹如何使用Python建立一個公共衛生新聞產生器。這個應用程式使用Streamlit建立網站，結合PubMed和Google Scholar搜索功能，並利用OpenAI的GPT模型生成新聞內容。

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
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={num_results}&format=json"
    search_response = requests.get(search_url).json()
    id_list = search_response['esearchresult']['idlist'] 
    results = []


    for pmid in id_list:
        fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        fetch_response = requests.get(fetch_url)
        soup = BeautifulSoup(fetch_response.content, 'xml')


        title = soup.find('ArticleTitle').text if soup.find('ArticleTitle') else 'N/A'
        abstract = soup.find('AbstractText').text if soup.find('AbstractText') else 'N/A'
       
        # Extract author information
        authors = []
        author_list = soup.find_all('Author')
        for author in author_list:
            last_name = author.find('LastName').text if author.find('LastName') else ''
            fore_name = author.find('ForeName').text if author.find('ForeName') else ''
            authors.append(f"{last_name} {fore_name}")
        
       
        # Extract journal information
        journal = soup.find('Journal')
        journal_title = journal.find('Title').text if journal and journal.find('Title') else 'N/A'
       
        results.append({
            'title': title,
            'abstract': abstract,
            'authors': ', '.join(authors) if authors else 'N/A',
            'journal': journal_title,
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        })
   
    return results
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
# Function to generate content with scientific references
def generate_content_with_references(prompt, topic, references):
    prompt += "\n\nPlease incorporate insights from these scientific sources in your response."
    for i, result in enumerate(references, 1):
        abstract = result.get('abstract', result.get('snippet', 'N/A'))
        prompt += f"\n{i}. {result['title']} : {abstract} - {result['url']}"
   
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a public health news journalist. When citing references in the text, use only the format [number]. At the end of the article, provide a full list of references using the format: [number] Title. Authors. Journal. URL"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message['content']
```

它接受一個提示、主題和參考資料列表，然後使用GPT模型生成包含參考文獻的內容。

## 6. 創建Streamlit應用界面
現在，我們開始創建Streamlit應用的界面：

```python
st.title('🩺📰 Public Health News Generator')
topic = st.text_input('News topic: ')
```

這裡創建了一個標題和一個輸入框，讓使用者輸入新聞主題。

## 7. 翻譯使用者輸入的主題
為了確保能夠處理不同語言的輸入，並且可以獲得更多的資訊，我們一律將輸入翻譯成英文：

```python
translator = Translator()
if topic:
    topic_en = translator.translate(topic, src='auto', dest='en').text
else:
    st.error('Please enter a news topic.')
    st.stop()
```

## 8. 生成新聞內容

輸入主題後，我們開始生成新聞內容：

```python
if topic:
    with st.spinner('Generating evidence-based article...'):
        # Search for scientific references only once
        pubmed_results = search_pubmed(topic_en)
        scholar_results = search_google_scholar(topic_en)
        references = pubmed_results + scholar_results

        intro_prompt = f"Produce an introduction and relevant information for a news article about {topic_en}. The content must be professional, based on scientific evidence, completely free of fabricated false content, and detailed, clear, and illustrated with examples."
        intro = generate_content_with_references(intro_prompt, topic_en, references)

        epidemiology_prompt = f"Provide epidemiological data related to {topic_en}:"
        epidemiology = generate_content_with_references(epidemiology_prompt, topic_en, references)

        causes_prompt = f"What are the causes of {topic_en}?"
        causes = generate_content_with_references(causes_prompt, topic_en, references)

        prevention_prompt = f"How can {topic_en} be prevented?"
        prevention = generate_content_with_references(prevention_prompt, topic_en, references)

        care_treatment_prompt = f"What are the care or treatment recommendations for {topic_en}?"
        care_treatment = generate_content_with_references(care_treatment_prompt, topic_en, references)

        # Generate the full article
        article_prompt = f"""You are a public health journalist and good at writing health news. Use the following information to write a news about {topic_en}. The news must be well organized, comprehensive, and well-structured. Include all the important points:

        Introduction: {intro}

        Epidemiology: {epidemiology}

        Causes: {causes}

        Prevention: {prevention}

        Care and Treatment: {care_treatment}

        Please structure the article with appropriate subheadings. End the article with a conclusion that summarizes the key points. After the conclusion, provide a list of references to reliable sources used in the article, which display with line breaks. Do not repeat any content."""

        article = generate_content_with_references(article_prompt, topic_en, references)

        # Generate the title
        title_prompt = f"Based on the following article, generate an engaging and informative title:\n\n{article}"
        title = generate_content_with_references(title_prompt, topic_en, references)
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

這樣，使用者就可以看到生成的中文新聞內容，同時也可以查看原始的英文版本。

通過以上步驟，我們創建了一個能夠根據用戶輸入的主題，自動生成基於科學證據的公共衛生新聞的應用程式。
