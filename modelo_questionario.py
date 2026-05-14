import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np

# =========================
# CARREGAR BASE DE DADOS
# =========================

url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"

df = pd.read_excel(url)

# =========================
# TRATAMENTO DOS DADOS
# =========================

df_encoded = pd.get_dummies(
    df,
    columns=[
        "Gender",
        "Ethnicity",
        "ParentalEducation"
    ],
    drop_first=True
)

# =========================
# DEFINIÇÃO DAS VARIÁVEIS
# =========================

y = df_encoded["GPA"]

X = df_encoded[[
    "Age",
    "StudyTimeWeekly",
    "Absences",
    "ParentalSupport",
    "Extracurricular"
]]

# =========================
# TREINAMENTO
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

modelo = LinearRegression()

modelo.fit(X_train, y_train)

# =========================
# MÉTRICAS
# =========================

y_pred = modelo.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)

# =========================
# FUNÇÃO DE PREVISÃO
# =========================

def prever_gpa(
    idade,
    horas_estudo,
    faltas,
    apoio_pais,
    extracurricular
):

    entrada = pd.DataFrame([{

        "Age": idade,

        "StudyTimeWeekly": horas_estudo,

        "Absences": faltas,

        "ParentalSupport": apoio_pais,

        "Extracurricular": extracurricular

    }])

    # adicionar colunas faltantes
    for coluna in X.columns:

        if coluna not in entrada.columns:
            entrada[coluna] = 0

    # mesma ordem do treino
    entrada = entrada[X.columns]

    previsao = modelo.predict(entrada)

    return previsao[0]