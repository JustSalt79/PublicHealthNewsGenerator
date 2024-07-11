import streamlit as st
from googletrans import Translator
import openai
import requests
from bs4 import BeautifulSoup
import re

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to search PubMed
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
        
        results.append({
            'title': title,
            'abstract': abstract,
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        })
    
    return results

# Function to search Google Scholar
def search_google_scholar(query, num_results=10):
    url = f"https://scholar.google.com/scholar?q={query}&num={num_results}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    results = []
    for item in soup.select('.gs_r.gs_or.gs_scl')[:num_results]:
        title_tag = item.select_one('.gs_rt')
        title = title_tag.text if title_tag else 'N/A'
        link = title_tag.a['href'] if title_tag and title_tag.a else 'N/A'
        snippet = item.select_one('.gs_rs').text if item.select_one('.gs_rs') else 'N/A'
        
        results.append({
            'title': title,
            'snippet': snippet,
            'url': link
        })
    
    return results

# Function to generate content with scientific references
def generate_content_with_references(prompt, topic):
    # Search for scientific references
    pubmed_results = search_pubmed(topic)
    scholar_results = search_google_scholar(topic)
    
    # Add references to the prompt
    prompt += "\n\nPlease incorporate insights from these scientific sources in your response:"
    for i, result in enumerate(pubmed_results + scholar_results):
        print(result['title'])
        prompt += f"\n{i+1}. {result['title']} : {result['abstract']} - {result['url']}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a public health news journalist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message['content']

# App UI framework
st.title('🩺📰 Evidence-Based Public Health News Generator')
topic = st.text_input('News topic: ')

# Translate user input to English
translator = Translator()
if topic:
    topic_en = translator.translate(topic, src='auto', dest='en').text
else:
    st.error('Please enter a news topic.')
    st.stop()

# Generate content for each section
if topic:
    with st.spinner('Generating evidence-based article...'):
        intro_prompt = f"Produce an introduction and relevant information for a news article about {topic_en}. The content must be professional, based on scientific evidence, completely free of fabricated false content, and detailed, clear, and illustrated with examples."
        intro = generate_content_with_references(intro_prompt, topic_en)

        epidemiology_prompt = f"Provide epidemiological data related to {topic_en}:"
        epidemiology = generate_content_with_references(epidemiology_prompt, topic_en)

        causes_prompt = f"What are the causes of {topic_en}?"
        causes = generate_content_with_references(causes_prompt, topic_en)

        prevention_prompt = f"How can {topic_en} be prevented?"
        prevention = generate_content_with_references(prevention_prompt, topic_en)

        care_treatment_prompt = f"What are the care or treatment recommendations for {topic_en}?"
        care_treatment = generate_content_with_references(care_treatment_prompt, topic_en)

        # Generate the full article
        article_prompt = f"""You are a public health journalist and good at writing health news. Use the following information to write a news about {topic_en}. The news must be well organized, comprehensive, and well-structured. Include all the important points:

        Introduction: {intro}

        Epidemiology: {epidemiology}

        Causes: {causes}

        Prevention: {prevention}

        Care and Treatment: {care_treatment}

        Please structure the article with appropriate headings and subheadings. End the article with a conclusion that summarizes the key points. After the conclusion, provide a list of references to reliable sources used in the article."""

        article = generate_content_with_references(article_prompt, topic_en)

        # Generate the title
        title_prompt = f"Based on the following article, generate an engaging and informative title:\n\n{article}"
        title = generate_content_with_references(title_prompt, topic_en)

        # Translate the article and title to Traditional Chinese
        translated_title = translator.translate(title, src='en', dest='zh-tw').text
        translated_article = translator.translate(article, src='en', dest='zh-tw').text

    # Display the results
    st.subheader(translated_title)
    st.write(translated_article)

    with st.expander('Original English Content'):
        st.subheader(title)
        st.write(article)
