import re
import string
import pandas as pd
import streamlit as st
import spacy
import nltk
import altair as alt
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Carrega o modelo do Spacy
nlp = spacy.load('pt_core_news_sm')

# Lista de entidades a serem excluídas
excluded_people = ['fulano', 'beltrano', 'sicrano']
excluded_places = ['lugar1', 'lugar2', 'lugar3']

# Função para limpar o texto
def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\b(pág|PÁG)\b", "", text)  # Remove "pág" ou "PÁG"
    text = re.sub(r"\b(camilo castelo branco)\b(?!')|(Camilo Castelo Branco)", "", text)  # Remove "camilo castelo branco" ou "Camilo Castelo Branco"
    text = re.sub(r"\s+", " ", text)  # Remove espaços em excesso
    text = text.strip()  # Remove espaços no início e no fim do texto

    # Tokenização do texto em palavras
    tokens = word_tokenize(text, language='portuguese')

    # Remoção de stopwords
    stop_words = set(stopwords.words('portuguese'))
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Remoção de sinais de pontuação
    tokens = [token for token in tokens if token not in string.punctuation]

    cleaned_text = ' '.join(tokens)

    return cleaned_text

# Função para extrair entidades
def extract_entities(cleaned_text, entity_type):
    doc = nlp(cleaned_text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ == entity_type:
            entity_text = ent.text.lower()
            if entity_text not in excluded_people and entity_text not in excluded_places:
                if entity_text == "em portugal":
                    entity_text = "portugal"
                if entity_text in entities:
                    entities[entity_text] += 1
                else:
                    entities[entity_text] = 1
    entity_data = {'Entity': list(entities.keys()), 'Frequency': list(entities.values())}
    return entity_data

# Interface do Streamlit
st.title("Análise de Texto")

# Dropdown para selecionar o arquivo de texto
selected_file = st.selectbox("Selecione o arquivo de texto", [
    "Camilo-A_Infanta_Capelista.txt",
    "Camilo-A_Gratidao.txt",
    "Camilo-Carlota_Angela.txt",
    "Camilo-Agostinho_de_Ceuta-Teatro"
])

# Carrega o texto do arquivo do GitHub
file_url = f"https://raw.githubusercontent.com/rlopesneto/AVD2023-Renato/main/{selected_file}"
response = requests.get(file_url)
text = response.text

# Limpa o texto
cleaned_text = clean_text(text)

# Extrai as entidades de pessoa
entities_people = extract_entities(cleaned_text, 'PER')

# Extrai as entidades de lugar
entities_places = extract_entities(cleaned_text, 'LOC')

# Cria um dataframe para os dados das entidades de pessoa
df_people = pd.DataFrame(entities_people)

# Filtra as entidades de pessoa com frequência maior que 2
df_filtered_people = df_people[df_people['Frequency'] > 2]

# Ordena o dataframe por frequência em ordem decrescente
df_sorted_people = df_filtered_people.sort_values(by='Frequency', ascending=False)

# Cria um gráfico de barras para visualizar a frequência de nomes de pessoas
chart_people = alt.Chart(df_sorted_people).mark_bar().encode(
    x='Entity',
    y='Frequency'
).properties(
    title='Frequência de Nomes de Pessoas',
    height=400
)

# Cria um dataframe para os dados das entidades de lugar
df_places = pd.DataFrame(entities_places)

# Filtra as entidades de lugar com frequência maior que 1
df_filtered_places = df_places[df_places['Frequency'] > 1]

# Ordena o dataframe por frequência em ordem decrescente
df_sorted_places = df_filtered_places.sort_values(by='Frequency', ascending=False)

# Cria um gráfico de barras para visualizar a frequência de nomes de lugares
chart_places = alt.Chart(df_sorted_places).mark_bar().encode(
    x='Entity',
    y='Frequency'
).properties(
    title='Frequência de Nomes de Lugares',
    height=400
)

# Exibe os gráficos
st.subheader("Frequência de Nomes de Pessoas")
st.altair_chart(chart_people, use_container_width=True)

st.subheader("Frequência de Nomes de Lugares")
st.altair_chart(chart_places, use_container_width=True)
