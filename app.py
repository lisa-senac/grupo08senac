import contextlib
import io
import runpy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns

from modelo_questionario import (
    OPCOES_APOIO_FAMILIAR,
    OPCOES_ESCOLARIDADE_PAIS,
    classificar_potencial_academico,
    cenarios_stress,
    metricas_validacao,
    monte_carlo_previsoes,
    prever_gpa,
    prever_gpa_dict,
)

st.set_page_config(
    page_title="Grupo 08 — Projeto integrador",
    layout="wide",
)


@st.cache_data
def carregar_dados():
    link = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
    return pd.read_excel(link)


st.title("Grupo 08 — Painel integrado")
st.caption(
    "Navegue pelas abas: dashboards originais do grupo, questionário de GPA e script de exploração."
)
st.divider()

tab_dash_faltas, tab_dash_indicadores, tab_questionario, tab_exploracao = st.tabs(
    [
        "Dashboard — Faltas e estudo",
        "Dashboard — GPA, engajamento e correlação",
        "Questionário e validação",
        "Exploração da regressão (saída texto)",
    ]
)

with tab_dash_faltas:
    # Ajusta o painel para ocupar a tela inteira

    # Cabeçalho da página
    st.title("Análise de Desempenho Escolar")
    st.markdown("Dashboard interativo do **Grupo 08**. O objetivo deste painel é apresentar quais fatores do dia a dia mais impactam a nota final (GPA) dos alunos.")
    st.divider() # Cria uma linha de separação

    # Função para buscar a planilha lá no Github do grupo
    # Salva os dados na variável 'df'
    df = carregar_dados()

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
        plt.close(fig1)

    with col_dir:
        st.info("O gráfico aponta uma queda drástica. Alunos que ultrapassam a marca de 20 faltas zeram suas chances de manter um bom GPA, independentemente do esforço extra.")

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
        plt.close(fig2)

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
    plt.close(fig3)

with tab_dash_indicadores:
    #--------------------------------
    #Configuração da página
    #--------------------------------

    st.title("Dashboards de Análise Acadêmica")
    st.markdown("Painéis de Média Geral de GPA, Taxa de Engajamento e Índice de Correlação.")
    st.divider()

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
        plt.close(fig1)

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
            plt.close(fig2)

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
        plt.close(fig3)

with tab_questionario:
    st.title("Questionário interativo para previsão de GPA")
    st.caption(
        "Projeto integrador — Grupo 08 · Regressão linear treinada sobre variáveis "
        "acadêmicas e comportamentais da base de desempenho escolar."
    )

    tab1, tab2 = st.tabs(
        [
            "11. Questionário e previsão",
            "12. Stress tests e validação",
        ]
    )

    MAPA_APOIO = dict(OPCOES_APOIO_FAMILIAR)
    MAPA_ESCOLARIDADE = dict(OPCOES_ESCOLARIDADE_PAIS)

    with tab1:
        st.header("Coleta de informações e simulação de cenário acadêmico")
        st.markdown(
            "Preencha os campos com o perfil do estudante. Os dados alimentam o "
            "**modelo de regressão linear** já treinado e geram uma **estimativa de "
            "GPA** (desempenho escolar geral), conforme as variáveis consideradas "
            "relevantes na etapa de modelagem.\n\n"
            "Na base utilizada, a **frequência escolar** não aparece como percentual "
            "isolado: ela é representada de forma **indireta** pelo total de **faltas** "
            "(quanto menor o número de faltas, maior a assiduidade esperada)."
        )

        idade = st.number_input(
            "Idade (anos)",
            min_value=14,
            max_value=30,
            value=17,
            help="Faixa etária compatível com a base original de estudantes.",
        )

        horas_estudo = st.slider(
            "Horas semanais dedicadas ao estudo fora da escola",
            0,
            40,
            10,
            help="Corresponde à variável de carga de estudo na base de dados.",
        )

        faltas = st.slider(
            "Quantidade de faltas (aulas)",
            0,
            50,
            5,
            help="Na base, este indicador substitui um campo explícito de frequência: "
            "muitas faltas implicam menor presença e tendem a penalizar o GPA previsto.",
        )

        rotulos_apoio = [t[0] for t in OPCOES_APOIO_FAMILIAR]
        apoio_pais = st.selectbox(
            "Nível de suporte familiar ao percurso escolar",
            rotulos_apoio,
            key="apoio",
            help="Apoio dos responsáveis em relação à rotina e ao acompanhamento pedagógico.",
        )

        extracurricular = st.selectbox(
            "Participação em atividades extracurriculares",
            ["Não", "Sim"],
            key="extra",
        )

        tutoring = st.selectbox(
            "Participação em reforço escolar ou aulas de apoio",
            ["Não", "Sim"],
            key="tutoring",
        )

        sports = st.selectbox(
            "Participação em esportes",
            ["Não", "Sim"],
            key="sports",
        )

        music = st.selectbox(
            "Participação em atividades musicais",
            ["Não", "Sim"],
            key="music",
        )

        volunteering = st.selectbox(
            "Participação em voluntariado",
            ["Não", "Sim"],
            key="volunteering",
        )

        rotulos_edu = [t[0] for t in OPCOES_ESCOLARIDADE_PAIS]
        parental_education = st.selectbox(
            "Escolaridade dos pais ou responsáveis",
            rotulos_edu,
            key="parental_education",
            help="Nível educacional associado ao contexto socioeconômico e de apoio ao estudo.",
        )

        if st.button("Gerar previsão de GPA", type="primary"):
            apoio_num = MAPA_APOIO[apoio_pais]
            parental_education_num = MAPA_ESCOLARIDADE[parental_education]
            extra_num = 1 if extracurricular == "Sim" else 0
            tutoring_num = 1 if tutoring == "Sim" else 0
            sports_num = 1 if sports == "Sim" else 0
            music_num = 1 if music == "Sim" else 0
            volunteering_num = 1 if volunteering == "Sim" else 0

            gpa = prever_gpa(
                idade,
                horas_estudo,
                faltas,
                apoio_num,
                extra_num,
                tutoring_num,
                sports_num,
                music_num,
                volunteering_num,
                parental_education_num,
            )

            st.subheader("Resultado da previsão")
            st.metric(
                label="GPA estimado pelo modelo",
                value=f"{gpa:.2f}",
                help="Saída numérica da regressão linear; interpretação qualitativa abaixo.",
            )

            st.markdown("**Interpretação qualitativa do potencial acadêmico**")
            texto, nivel = classificar_potencial_academico(gpa)
            if nivel == "error":
                st.error(texto)
            elif nivel == "warning":
                st.warning(texto)
            else:
                st.success(texto)

            st.caption(
                "As três faixas textuais aproximam o roteiro do projeto (faculdade mediana, "
                "boa faculdade, alta competitividade), calibradas pelos **tercis do GPA** na "
                "amostra de treino — assim a classificação acompanha a distribuição empírica "
                "e não cortes fixos arbitrários."
            )

    with tab2:
        st.header("Robustez do modelo e validação estatística")
        st.markdown(
            "Conforme o roteiro do projeto, esta seção apoia a **validação do modelo "
            "preditivo** e os **testes de stress**: primeiro avaliam-se erros no conjunto "
            "de teste; em seguida, perfis extremos e intermediários; por fim, uma "
            "**simulação de Monte Carlo** verifica a dispersão das previsões quando as "
            "entradas variam aleatoriamente dentro de limites plausíveis na base."
        )

        st.subheader("Separação treino / teste e métricas de erro")
        met = metricas_validacao()
        c1, c2, c3 = st.columns(3)
        c1.metric("MAE (erro absoluto médio)", f"{met['mae']:.4f}")
        c2.metric("RMSE (raiz do erro quadrático médio)", f"{met['rmse']:.4f}")
        c3.metric("R² (coeficiente de determinação)", f"{met['r2']:.4f}")
        st.caption(
            "Os dados foram divididos em **80% treino** e **20% teste** "
            "(train_test_split do scikit-learn, random_state=42). MAE e RMSE estão na "
            "mesma unidade do GPA; o R² mede a fração da variância do GPA explicada no "
            "conjunto de teste."
        )

        st.subheader("Simulação de cenários de stress na fronteira da base")
        st.markdown(
            "Foram montados três perfis sintéticos combinando **valores extremos e "
            "tendências centrais** observados na base: (1) forte dedicação ao estudo, "
            "poucas faltas e alto suporte familiar; (2) combinação intermediária; "
            "(3) baixa dedicação, muitas faltas e menor suporte. Os rótulos abaixo "
            "resumem cada combinação; os campos JSON repetem os nomes das variáveis do "
            "modelo para conferência técnica."
        )
        cenarios = cenarios_stress()
        for nome, vals in cenarios.items():
            g = prever_gpa_dict(vals)
            interp, _ = classificar_potencial_academico(g)
            with st.expander(nome):
                st.json(vals)
                st.write(f"**GPA previsto pelo modelo:** {g:.2f}")
                st.write(f"**Leitura qualitativa:** {interp}")

        st.subheader("Monte Carlo: consistência das previsões sob incerteza nas entradas")
        st.markdown(
            "Em cada replicação, **todas** as variáveis de entrada são sorteadas de "
            "forma **independente** entre o mínimo e o máximo observados na base; "
            "variáveis binárias assumem apenas **0 ou 1**. O objetivo é inspecionar se "
            "as previsões permanecem em faixa razoável ou se o modelo reage com "
            "instabilidade (dispersão excessiva) a combinações atípicas porém limitadas "
            "aos dados reais."
        )
        n_mc = st.number_input(
            "Número de replicações da simulação",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100,
            key="n_mc",
        )
        if st.button("Executar simulação de Monte Carlo"):
            with st.spinner("Executando replicações aleatórias…"):
                mc = monte_carlo_previsoes(n_iter=int(n_mc), random_state=42)
            st.markdown(
                f"**Estatísticas descritivas das previsões simuladas:** média "
                f"{mc['media']:.3f} · desvio-padrão {mc['desvio']:.3f} · mínimo "
                f"{mc['min']:.3f} · máximo {mc['max']:.3f} · percentis 5 e 95 "
                f"({mc['p5']:.3f} — {mc['p95']:.3f})."
            )
            counts, edges = np.histogram(mc["previsoes"], bins=32)
            centros = (edges[:-1] + edges[1:]) / 2
            largura = float(edges[1] - edges[0])
            fig, ax = plt.subplots(figsize=(9, 3.2))
            ax.bar(centros, counts, width=largura * 0.92, color="steelblue")
            ax.set_xlabel("GPA previsto em cada replicação")
            ax.set_ylabel("Número de replicações (frequência)")
            ax.set_title("Histograma das previsões — abordagem de Monte Carlo")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

with tab_exploracao:
    st.header("Exploração da regressão (script original)")
    st.markdown(
        "Mesmo fluxo do arquivo **exploracao_regressao.py** (antigo **app.py**): "
        "one-hot encoding, treino e texto no console."
    )
    p_script = Path(__file__).resolve().parent / "exploracao_regressao.py"
    if st.button("Executar script e mostrar saída", key="btn_run_exploracao"):
        buf = io.StringIO()
        with st.spinner("Executando..."):
            with contextlib.redirect_stdout(buf):
                runpy.run_path(str(p_script), run_name="__exploracao__")
        st.code(buf.getvalue() or "(sem saída)", language=None)
