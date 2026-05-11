"""
Projeto Integrador - Grupo 08
Análise de Fatores de Sucesso Acadêmico - Dashboard (Faltas x Desempenho)
Matheus Santos Cruz
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ajusta o painel para ocupar a tela inteira
st.set_page_config(page_title="Dashboard - Grupo 08", layout="wide")

# Cabeçalho da página
st.title("Análise de Desempenho Escolar")
st.markdown("Dashboard interativo do **Grupo 08**. O objetivo deste painel é apresentar quais fatores do dia a dia mais impactam a nota final (GPA) dos alunos.")
st.divider() # Cria uma linha de separação

# Função para buscar a planilha lá no Github do grupo
@st.cache_data
def puxar_dados():
    link = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
    return pd.read_excel(link)

# Salva os dados na variável 'df'
df = puxar_dados()

# ==========================================
# 1. INDICADORES RÁPIDOS (KPIs)
# ==========================================
st.subheader("Visão Geral da Base de Dados")

# Separando em 3 colunas para ficar um do lado do outro
col1, col2, col3 = st.columns(3)

# Fazendo os cálculos básicos
media_notas = df['GPA'].mean()
media_faltas = df['Absences'].mean()
correlacao = df['Absences'].corr(df['GPA'])

# Colocando na tela
col1.metric("Média Geral de Notas (GPA)", f"{media_notas:.2f}")
col2.metric("Média de Faltas", f"{media_faltas:.0f} aulas")
col3.metric("Correlação: Faltas x Nota", f"{correlacao:.2f}", "Impacto Negativo")

st.divider()

# ==========================================
# 2. O PROBLEMA DAS FALTAS
# ==========================================
st.subheader("O Impacto das Faltas nas Notas")
st.markdown("Ao cruzar os dados, percebemos que a frequência escolar é o fator que mais pesa no boletim do aluno.")

col_esq, col_dir = st.columns([2, 1])

with col_esq:
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    
    # Gráfico de dispersão mostrando faltas x notas
    sns.regplot(
        data=df, x="Absences", y="GPA", 
        scatter_kws={'alpha': 0.3, 'color': 'red'}, 
        line_kws={'color': 'black'}, ax=ax1
    )
    
    ax1.set_xlabel("Quantidade Total de Faltas")
    ax1.set_ylabel("Nota (GPA)")
    st.pyplot(fig1)

with col_dir:
    st.info("O gráfico aponta uma queda drástica. Alunos que ultrapassam a marca de 20 faltas zaram suas chances de manter um bom GPA, independentemente do esforço extra.")

st.divider()

# ==========================================
# 3. COMPROVANDO A IMPORTÂNCIA DO ESTUDO
# ==========================================
st.subheader("O tempo de estudo faz diferença?")
st.markdown("Para provar a nossa teoria de que estudar funciona, criamos um filtro: removemos os alunos muito faltosos e analisamos apenas os **assíduos** (menos de 5 faltas).")

# Filtra a base original pegando só quem faltou menos de 5 vezes
df_assiduos = df[df['Absences'] < 5]

col_esq2, col_dir2 = st.columns([1, 2])

with col_esq2:
    st.success("Avaliando apenas alunos com boa presença, a linha de tendência muda completamente. Isso prova que estudar em casa aumenta a nota, desde que o aluno frequente as aulas.")

with col_dir2:
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    
    # Gráfico de estudo x notas (apenas para assíduos)
    sns.regplot(
        data=df_assiduos, x="StudyTimeWeekly", y="GPA", 
        scatter_kws={'alpha': 0.5, 'color': 'blue'}, 
        line_kws={'color': 'black'}, ax=ax2
    )
    
    ax2.set_xlabel("Horas de Estudo Semanais")
    ax2.set_ylabel("Nota (GPA)")
    st.pyplot(fig2)

st.divider()

# ==========================================
# 4. MAPA DE CALOR
# ==========================================
st.subheader("Mapa de Correlações")
st.markdown("Um resumo técnico das variáveis escolhidas para o modelo preditivo.")

fig3, ax3 = plt.subplots(figsize=(8, 4))

# Pegando só as colunas importantes para não poluir o visual
colunas_foco = df[['GPA', 'Absences', 'ParentalSupport', 'StudyTimeWeekly', 'Tutoring']]

# Desenhando o mapa
sns.heatmap(
    colunas_foco.corr(), 
    annot=True, cmap="Blues", fmt=".2f", 
    linewidths=0.5, ax=ax3
)
st.pyplot(fig3)