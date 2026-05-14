import streamlit as st

st.set_page_config(
    page_title="Previsão de GPA",
    layout="centered"
)

st.title("Sistema de Previsão Acadêmica")

# Criando abas
tab1, tab2 = st.tabs([
    "Questionário GPA",
    "Stress Tests"
])


with tab1:

    st.header("Previsão de Desempenho Acadêmico")

    idade = st.number_input(
        "Qual sua idade?",
        min_value=14,
        max_value=30,
        value=17
    )

    horas_estudo = st.slider(
        "Quantas horas você estuda por semana?",
        0,
        40,
        10
    )

    faltas = st.slider(
        "Quantidade de faltas",
        0,
        50,
        5
    )

    apoio_pais = st.selectbox(
        "Nível de suporte dos pais",
        ["Baixo", "Médio", "Alto"],
        key="apoio"
    )

    extracurricular = st.selectbox(
        "Participa de atividades extracurriculares?",
        ["Não", "Sim"],
        key="extra"
    )

    if st.button("Prever GPA"):

        mapa_apoio = {
            "Baixo": 0,
            "Médio": 1,
            "Alto": 2
        }

        apoio_num = mapa_apoio[apoio_pais]

        extra_num = 1 if extracurricular == "Sim" else 0

        gpa = (
            500
            + horas_estudo * 12
            - faltas * 4
            + apoio_num * 35
            + extra_num * 20
        )

        st.success(f"Seu GPA provável é: {gpa:.0f}")

        if gpa < 600:
            st.error("Potencial para faculdade mediana")

        elif gpa < 750:
            st.warning("Potencial para boa faculdade")

        else:
            st.success("Potencial para faculdade excelente")

with tab2:

    st.header("Testes de Stress e Validação")

    st.write(
        "Simulação de cenários extremos para "
        "avaliar a estabilidade do modelo."
    )

    cenario = st.selectbox(
        "Escolha um cenário",
        [
            "Aluno Excelente",
            "Aluno Mediano",
            "Aluno de Risco"
        ]
    )

    if cenario == "Aluno Excelente":

        st.success("Resultado esperado: GPA elevado")

        st.write("""
        Características:
        - Muitas horas de estudo
        - Poucas faltas
        - Alto suporte familiar
        """)

    elif cenario == "Aluno Mediano":

        st.warning("Resultado esperado: GPA intermediário")

        st.write("""
        Características:
        - Horas moderadas de estudo
        - Frequência regular
        - Suporte médio
        """)

    else:

        st.error("Resultado esperado: GPA baixo")

        st.write("""
        Características:
        - Poucas horas de estudo
        - Muitas faltas
        - Baixo suporte
        """)