# PublicHealth article generator
透過AI model 我們可以輸入關鍵字後依據想要的內容設計提詞 產生出文章 

這個教程將介紹如何使用Python、Streamlit、Google Translate和OpenAI API來建立一個公共衛生新聞生成器。
這個應用程式可以根據用戶輸入的主題自動生成公共衛生相關的新聞文章，並將其翻譯成繁體中文。

## 目錄
1. [程式概述](#程式概述)
2. [所需套件](#所需套件)
3. [設置OpenAI API密鑰](#設置OpenAI-API密鑰)
4. [應用程式界面](#應用程式界面)
5. [翻譯功能](#翻譯功能)
6. [內容生成功能](#內容生成功能)
7. [生成文章各部分](#生成文章各部分)
8. [組合完整文章](#組合完整文章)
9. [顯示結果](#顯示結果)
10. [總結](#總結)

## 程式概述

這個程式使用Streamlit建立一個簡單的網頁介面，讓用戶輸入一個公共衛生相關的主題。然後，它使用OpenAI的GPT-4模型生成一篇關於該主題的詳細新聞文章，包括引言、流行病學數據、原因、預防方法以及護理和治療建議。最後，程式將生成的內容翻譯成繁體中文並顯示結果。

## 所需套件

首先，我們需要導入必要的Python套件：

```python
import streamlit as st
from googletrans import Translator
import openai
```

- `streamlit`：用於創建網頁應用程式介面
- `googletrans`：用於翻譯文本
- `openai`：用於與OpenAI API進行交互

## 設置OpenAI API密鑰

為了使用OpenAI的服務，我們需要設置API密鑰：

```python
openai.api_key = st.secrets["OPENAI_API_KEY"]
```

這裡我們使用Streamlit的secrets管理功能來安全地存儲API密鑰。
(另外設置secrets.toml來儲存我們的API KEY)

## 應用程式界面

使用Streamlit創建一個簡單的用戶界面：

```python
# App UI framework
st.title('🩺📰 Public Health News Generator')
topic = st.text_input('News topic: ')
```

這將顯示一個標題和一個文本輸入框，讓用戶輸入新聞主題。

## 翻譯功能

使用Google Translate API將用戶輸入的主題翻譯成英文：

```python
# Translate user input to English
translator = Translator()
if topic:
    topic_en = translator.translate(topic, src='auto', dest='en').text
else:
    st.error('Please enter a news topic.')
    st.stop()
```

這段代碼檢查用戶是否輸入了主題，如果有，則將其翻譯成英文；如果沒有，則顯示錯誤消息並停止程式執行。

## 內容生成功能

定義一個函數來使用OpenAI API生成內容：

```python
def generate_content(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a public health news expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message['content']
```

這個函數接受一個提示作為輸入，使用GPT-4模型生成回應，並返回生成的內容。

## 生成文章各部分

使用`generate_content`函數生成文章的各個部分：

```python
# Generate content for each section
if topic:
    with st.spinner('Generating article...'):
        intro_prompt = f"Produce an introduction and relevant information for a news article about {topic_en}. The content must be professional, based on scientific evidence, completely free of fabricated false content, and detailed, clear, and illustrated with examples."
        intro = generate_content(intro_prompt)

        epidemiology_prompt = f"Provide epidemiological data related to {topic_en}:"
        epidemiology = generate_content(epidemiology_prompt)

        causes_prompt = f"What are the causes of {topic_en}?"
        causes = generate_content(causes_prompt)

        prevention_prompt = f"How can {topic_en} be prevented?"
        prevention = generate_content(prevention_prompt)

        care_treatment_prompt = f"What are the care or treatment recommendations for {topic_en}?"
        care_treatment = generate_content(care_treatment_prompt)
```

這段代碼為文章的每個部分（引言、流行病學、原因、預防、護理和治療）生成內容。

## 組合完整文章

將各個部分組合成一個完整的文章：

```python
# Generate the full article
        article_prompt = f"""Using the following information about {topic_en}, please organize and write a comprehensive, well-structured article. Include all the important points but ensure the article flows naturally:

        Introduction: {intro}

        Epidemiology: {epidemiology}

        Causes: {causes}

        Prevention: {prevention}

        Care and Treatment: {care_treatment}

        Please structure the article with appropriate headings and subheadings. End the article with a conclusion that summarizes the key points. After the conclusion, provide a list of references to reliable sources used in the article."""

        article = generate_content(article_prompt)

        # Generate the title
        title_prompt = f"Based on the following article, generate an engaging and informative title:\n\n{article}"
        title = generate_content(title_prompt)
```

這段代碼將所有生成的內容組合成一篇完整的文章，並為文章生成一個標題。

## 顯示結果

最後，將生成的文章和標題翻譯成繁體中文，並顯示結果：

```python
# Translate the article and title to Traditional Chinese
        translated_title = translator.translate(title, src='en', dest='zh-tw').text
        translated_article = translator.translate(article, src='en', dest='zh-tw').text

    # Display the results
    st.subheader(translated_title)
    st.write(translated_article)

    with st.expander('Original English Content'):
        st.subheader(title)
        st.write(article)
```

這段代碼將生成的英文內容翻譯成繁體中文，顯示翻譯後的內容，並提供一個可展開的部分來查看原始英文內容。

## 總結

這個程式展示了如何結合多個API和工具來創建一個強大的公共衛生新聞生成器。它利用了OpenAI的GPT-4模型來生成高質量的內容，Google Translate API來處理多語言支持，以及Streamlit來創建一個用戶友好的網頁界面。這種應用可以在快速生成特定主題的公共衛生資訊方面非常有用，特別是在需要多語言內容的情況下。
