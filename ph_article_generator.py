import streamlit as st
from googletrans import Translator
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App UI framework
st.title('🩺📰 Public Health News Generator')
topic = st.text_input('News topic: ')

# Translate user input to English
translator = Translator()
if topic:
    topic_en = translator.translate(topic, src='auto', dest='en').text
else:
    st.error('Please enter a news topic.')
    st.stop()

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

        # Translate the article and title to Traditional Chinese
        translated_title = translator.translate(title, src='en', dest='zh-tw').text
        translated_article = translator.translate(article, src='en', dest='zh-tw').text

    # Display the results
    st.subheader(translated_title)
    st.write(translated_article)

    with st.expander('Original English Content'):
        st.subheader(title)
        st.write(article)