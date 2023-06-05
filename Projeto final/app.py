import streamlit as st
import altair as alt
import pandas as pd

# Título do aplicativo
st.title('Aplicativo de Visualização de Dados')

# Upload do arquivo CSV
st.subheader('Carregar arquivo CSV')
uploaded_file = st.file_uploader('Selecione um arquivo CSV', type='csv')

if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)

    # Exibindo o DataFrame
    st.subheader('Dados')
    st.write(df)

    # Seleção de colunas para os eixos X e Y
    x_axis = st.selectbox('Selecione o eixo X', df.columns)
    y_axis = st.selectbox('Selecione o eixo Y', df.columns)

    # Gráfico de dispersão interativo com Altair
    st.subheader('Gráfico de Dispersão')
    scatter_chart = alt.Chart(df).mark_circle().encode(
        x=x_axis,
        y=y_axis,
        tooltip=list(df.columns)
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)

    # Gráfico de barras interativo com Altair
    st.subheader('Gráfico de Barras')
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=x_axis,
        y=y_axis,
        tooltip=list(df.columns)
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Gráfico de linha 
    st.subheader('Gráfico de Linha')
    line_chart = alt.Chart(df).mark_line().encode(
        x=x_axis,
        y=y_axis,
        tooltip=list(df.columns)
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)
    
    # Gráfico de área 
    st.subheader('Gráfico de Área')
    area_chart = alt.Chart(df).mark_area().encode(
        x=x_axis,
        y=y_axis,
        tooltip=list(df.columns)
    ).interactive()
    st.altair_chart(area_chart, use_container_width=True)
