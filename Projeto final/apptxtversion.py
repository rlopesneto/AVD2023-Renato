import re
import sys
import matplotlib.pyplot as plot
import streamlit as st
import pandas as pd
import altair as alt

POL = {}

# Rest of the code remains the same...


POL = {}

def carrega_sentilex():
    with open("sentilexjj.txt") as f:
        for linha in f:
            linha = re.sub(r"ANOT=.*", "", linha)
            lista = re.split(r";",linha)
            if len(lista) == 5:
                pallemapos, flex, assina, pol, lixo = lista
                pal = re.split(r",",pallemapos)[0]
                pol = int( re.sub(r"POL:N[01]=", "", pol) )
                POL[pal] = pol
            elif len(lista) == 6:
                pallemapos, flex, assina, pol1, pol2, lixo = lista
                pal = re.split(r",",pallemapos)[0]
                pol1 = int( re.sub(r"POL:N[01]=", "", pol1) )
                pol2 = int( re.sub(r"POL:N[01]=", "", pol2) )
                POL[pal] = (pol1+pol2)/2 
            else:
                print(lista)
                exit()

def sentimento(frase):
    lp = re.findall(r"\w+", frase)
    ptotalneg = 0 
    ptotalpos = 0
    qp = 0
    qn = 0

    for p in lp:
        if p in POL:
            v = POL[p]
            if  v > 0: 
                ptotalpos += v
                qp += 1

            if  v < 0: 
                ptotalneg += -v
                qn += 1

    return (ptotalpos, qp, ptotalneg, qn, len(lp))

def criagraf(xl, y):
    plot.bar(xl, y, color="red")
    plot.show()
    plot.savefig("g.png")

def main():
    st.title('Aplicativo de Análise de Sentimentos')

    # Upload do arquivo TXT
    st.subheader('Carregar arquivo TXT')
    uploaded_file = st.file_uploader('Selecione um arquivo TXT', type='txt')

    if uploaded_file is not None:
        txt = uploaded_file.read().decode('utf-8')
        ptotalpos, qp, ptotalneg, qn, np = sentimento(txt)
        Factor = ptotalpos / ptotalneg
        st.write(f"Número de caracteres: {len(txt)}")
        st.write(f"Total positivo: {ptotalpos}")
        st.write(f"Quantidade de palavras positivas: {qp}")
        st.write(f"Total negativo: {ptotalneg}")
        st.write(f"Quantidade de palavras negativas: {qn}")
        st.write(f"Total de palavras: {np}")
        st.write(f"Fator: {Factor}")

        listacap = re.split(r"#", txt)

        df_data = []
        for n, cap in enumerate(listacap):
            ptotalpos, qp, ptotalneg, qn, np = sentimento(cap)
            sentcap = ((ptotalpos-(ptotalneg*Factor))/np)*1000
            df_data.append({
                'Cap': f'C{n}',
                'Nº caracteres': len(cap),
                'totpos': ptotalpos,
                'quanpos': qp,
                'totneg': ptotalneg,
                'quanneg': qn,
                'palavras': np,
                'rationeg': Factor,
                'sentcap': sentcap
            })

        df = pd.DataFrame(df_data)
        st.subheader('Dados do Sentimento por Capítulo')
        st.write(df)

        # Gráfico de barras interativo com Altair
        st.subheader('Gráfico de Barras')
        bar_chart = alt.Chart(df).mark_bar().encode(
            x='Cap',
            y='sentcap',
            tooltip=list(df.columns)
        ).interactive()
        st.altair_chart(bar_chart, use_container_width=True)

        # Exportar DataFrame para CSV
        st.subheader('Exportar para CSV')
        csv_file = st.text_input('Nome do arquivo CSV', value='output.csv')
        if st.button('Exportar'):
            df.to_csv(csv_file, index=False)
            st.success(f'O arquivo CSV "{csv_file}" foi exportado com sucesso.')

        # Gráfico de linha usando matplotlib
        st.subheader('Gráfico de Linha - Análise de Sentimentos')
        criagraf(df['Cap'].tolist()[1:], df['sentcap'].tolist()[1:])


carrega_sentilex()
main()
