import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

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
    page_title="Grupo 08 — Questionário GPA",
    layout="centered",
)

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
