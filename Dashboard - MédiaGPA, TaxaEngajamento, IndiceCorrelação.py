"""
Grupo 8 - Projeto Integrador
Aluno: Erick Massahiro Yamamoto
Dashboard: Média geral de GPA, Taxa de engajamento, Índice de correlação
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

#--------------------------------
#Configuração da página
#--------------------------------
st.set_page_config(page_title="Dashboards Acadêmicos", layout="wide")

st.title("Dashboards de Análise Acadêmica")
st.markdown("Painéis de Média Geral de GPA, Taxa de Engajamento e Índice de Correlação.")
st.divider()

@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
    return pd.read_excel(url)

df = carregar_dados()

#--------------------------------
#Dashboard 1: Média geral de GPA
#--------------------------------
st.header("1 - Média Geral de GPA (Nota)")
media_gpa = df["GPA"].mean()

col1_txt, col1_graf = st.columns([1, 2])
with col1_txt:
    st.metric(label="Média Geral", value=f"{media_gpa:.2f}")

with col1_graf:
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    ax1.hist(df["GPA"], bins=20, color='skyblue', edgecolor='black')
    ax1.axvline(media_gpa, color='red', linestyle='dashed', linewidth=2, label=f'Média: {media_gpa:.2f}')
    ax1.set_title("Distribuição das Notas (GPA)")
    ax1.set_xlabel("GPA")
    ax1.set_ylabel("Quantidade de Alunos")
    ax1.legend()
    st.pyplot(fig1)

st.divider()

#---------------------------------
#Dashboard 2: Taxa de engajamento
#---------------------------------
st.header("2 - Taxa de Engajamento")

coluna_alvo = "Extracurricular"

if coluna_alvo in df.columns:
    engajados = df[df[coluna_alvo] == 1].shape[0]
    nao_engajados = df[df[coluna_alvo] == 0].shape[0]
    taxa_engajamento = (engajados / len(df)) * 100

    col2_txt, col2_graf = st.columns([1, 2])
    with col2_txt:
        st.metric(label="Alunos Engajados", value=f"{taxa_engajamento:.1f}%")
        st.info("Percentual de alunos que participam ativamente de atividades extracurriculares em comparação aos que não participam.")

    with col2_graf:
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        labels = ['Participam (Engajados)', 'Não Participam']
        valores = [engajados, nao_engajados]
        cores = ["#02C00B", "#FF0000"]
        ax2.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=cores)
        ax2.axis('equal')
        st.pyplot(fig2)

st.divider()

#----------------------------------
#Dashboard 3: Índice de correlação
#----------------------------------
st.header("3 - Índice de Correlação")
correlacao = df["StudyTimeWeekly"].corr(df["GPA"])

col3_txt, col3_graf = st.columns([1, 2])
with col3_txt:
    st.metric(label="Índice de Correlação", value=f"{correlacao:.3f}")
    if correlacao > 0:
        st.success("Temos uma correlação positiva. Isso indica que, quanto mais horas o aluno estuda, maior tende a ser a sua nota final.")
    else:
        st.warning("A correlação não é fortemente positiva.")

with col3_graf:
    fig3, ax3 = plt.subplots(figsize=(8, 3))
    ax3.scatter(df["StudyTimeWeekly"], df["GPA"], alpha=0.5, color='purple')
    ax3.set_title("Relação: Horas de Estudo vs GPA")
    ax3.set_xlabel("Horas de Estudo por Semana")
    ax3.set_ylabel("Nota Final (GPA)")
    ax3.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig3)