"""
modelo_questionario.py  —  Grupo 08 · Projeto Integrador
=========================================================
Treina a regressão linear com o MESMO pipeline de exploracao_regressao.py:
  • One-Hot Encoding em Gender, Ethnicity e ParentalEducation (drop_first=True)
  • Remove GradeClass e StudentID
  • Divisão 80/20 (random_state=42)

ESCALONAMENTO DAS PREVISÕES
----------------------------
  A regressão linear produz previsões numa faixa estreita (~1.5–2.1) porque
  os coeficientes são pequenos (R² ~0.15–0.20). Aplicamos escalonamento
  min-max sobre o conjunto de treino para mapear proporcionalmente para 0–4,
  preservando a ordem relativa entre perfis.

CLASSIFICAÇÃO FINAL — definida pelo Grupo 08 (contexto: ingresso em faculdades):
  GPA >= 3.0        →  Alto / Médio Padrão       (alta competitividade)
  2.0 <= GPA < 3.0  →  Baixo Padrão / Limite de Aprovação
  GPA < 2.0         →  Risco de Não Passar / Reprovação
"""

from __future__ import annotations

import io
import urllib.request

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------------
# 1. Constantes expostas para o app.py
# ---------------------------------------------------------------------------

OPCOES_APOIO_FAMILIAR: list[tuple[str, int]] = [
    ("Nenhum",     0),
    ("Baixo",      1),
    ("Moderado",   2),
    ("Alto",       3),
    ("Muito Alto", 4),
]

OPCOES_ESCOLARIDADE_PAIS: list[tuple[str, int]] = [
    ("Sem escolaridade formal", 0),
    ("Ensino Fundamental",      1),
    ("Ensino Médio",            2),
    ("Ensino Superior",         3),
    ("Pós-graduação",           4),
]

# ---------------------------------------------------------------------------
# 2. Carregamento e treinamento
# ---------------------------------------------------------------------------

_URL = (
    "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/"
    "Student_performance_data.xlsx"
)


def _baixar_df() -> pd.DataFrame:
    req = urllib.request.Request(
        _URL, headers={"User-Agent": "Mozilla/5.0 (grupo08)"}
    )
    raw = urllib.request.urlopen(req, timeout=30).read()
    return pd.read_excel(io.BytesIO(raw))


def _treinar():
    df = _baixar_df()

    df_enc = pd.get_dummies(
        df,
        columns=["Gender", "Ethnicity", "ParentalEducation"],
        drop_first=True,
    )

    y = df_enc["GPA"]
    X = df_enc.drop(columns=["GPA", "GradeClass", "StudentID"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Intervalo das previsões brutas no treino — base do escalonamento
    preds_treino = modelo.predict(X_train)
    pred_min = float(preds_treino.min())
    pred_max = float(preds_treino.max())

    return modelo, list(X.columns), X_test, y_test, pred_min, pred_max


_modelo, _colunas_X, _X_test, _y_test, _pred_min, _pred_max = _treinar()


# ---------------------------------------------------------------------------
# 3. Escalonamento interno — mapeia previsão bruta para escala 0–4
# ---------------------------------------------------------------------------

def _escalonar(gpa_bruto: float) -> float:
    """
    Mapeia a previsão bruta da regressão para a escala 0–4,
    preservando a proporção relativa entre os perfis.
    """
    if _pred_max == _pred_min:
        return 2.0
    escalado = (gpa_bruto - _pred_min) / (_pred_max - _pred_min) * 4.0
    return float(np.clip(escalado, 0.0, 4.0))


# ---------------------------------------------------------------------------
# 4. Funções públicas
# ---------------------------------------------------------------------------

def prever_gpa(
    idade: int,
    horas_estudo: float,
    faltas: int,
    apoio_pais: int,
    extracurricular: int,
    tutoring: int,
    sports: int,
    music: int,
    volunteering: int,
    parental_education: int,
) -> float:
    """Retorna o GPA estimado na escala 0–4."""
    entrada: dict[str, float] = {col: 0.0 for col in _colunas_X}

    entrada["Age"]             = float(idade)
    entrada["StudyTimeWeekly"] = float(horas_estudo)
    entrada["Absences"]        = float(faltas)
    entrada["ParentalSupport"] = float(apoio_pais)
    entrada["Extracurricular"] = float(extracurricular)
    entrada["Tutoring"]        = float(tutoring)
    entrada["Sports"]          = float(sports)
    entrada["Music"]           = float(music)
    entrada["Volunteering"]    = float(volunteering)

    for nivel in [1, 2, 3, 4]:
        col = f"ParentalEducation_{nivel}"
        if col in entrada:
            entrada[col] = 1.0 if parental_education == nivel else 0.0

    X_novo = pd.DataFrame([entrada])[_colunas_X]
    gpa_bruto = float(_modelo.predict(X_novo)[0])
    return _escalonar(gpa_bruto)


def prever_gpa_dict(valores: dict) -> float:
    return prever_gpa(**valores)


def classificar_potencial_academico(gpa: float) -> tuple[str, str]:
    """
    Classificação definida pelo Grupo 08 — contexto de ingresso em faculdades.

    Faixas (escala 0–4):
      GPA >= 3.0        →  Alto / Médio Padrão (alta competitividade)
      2.0 <= GPA < 3.0  →  Baixo Padrão / Limite de Aprovação
      GPA < 2.0         →  Risco de Não Passar / Reprovação
    """
    if gpa >= 3.0:
        texto = (
            "✅ GPA estimado: Alto / Médio Padrão (3.0 a 4.0).\n\n"
            "O perfil indica potencial para ingresso em faculdades de alta "
            "competitividade. Manter a frequência escolar e as horas de estudo "
            "são os fatores decisivos para sustentar este nível."
        )
        return texto, "success"
    elif gpa >= 2.0:
        texto = (
            "⚠️ GPA estimado: Baixo Padrão / Limite de Aprovação (2.0 a 2.9).\n\n"
            "O perfil indica desempenho no limite para ingresso em faculdades "
            "medianas. Reduzir faltas e aumentar as horas de estudo semanais são "
            "as ações com maior impacto para subir de faixa."
        )
        return texto, "warning"
    else:
        texto = (
            "🚨 GPA estimado: Risco de Não Passar / Reprovação (abaixo de 2.0).\n\n"
            "O perfil indica risco elevado de reprovação e baixa chance de ingresso "
            "em faculdades. Reduzir faltas urgentemente e aumentar significativamente "
            "a dedicação aos estudos são as intervenções prioritárias."
        )
        return texto, "error"


def metricas_validacao() -> dict:
    """
    MAE, RMSE e R² calculados sobre as previsões brutas (sem escalonamento),
    refletindo fielmente a qualidade estatística do modelo original.
    """
    y_pred = _modelo.predict(_X_test)
    mae  = float(mean_absolute_error(_y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(_y_test, y_pred)))
    r2   = float(r2_score(_y_test, y_pred))
    return {"mae": mae, "rmse": rmse, "r2": r2}


def cenarios_stress() -> dict[str, dict]:
    """
    Três perfis sintéticos para o stress test, conforme o planejamento do grupo.
    Valores dentro dos limites reais do dataset:
      StudyTimeWeekly : 0–20h
      Absences        : 0–29
      ParentalSupport : 0–4
      ParentalEducation: 0–4
    """
    return {
        "🟢 Perfil Alta Performance — dedicação máxima, poucas faltas": {
            "idade": 17,
            "horas_estudo": 20,
            "faltas": 0,
            "apoio_pais": 4,
            "extracurricular": 1,
            "tutoring": 1,
            "sports": 1,
            "music": 0,
            "volunteering": 1,
            "parental_education": 4,
        },
        "🟡 Perfil Intermediário — esforço moderado": {
            "idade": 17,
            "horas_estudo": 10,
            "faltas": 10,
            "apoio_pais": 2,
            "extracurricular": 1,
            "tutoring": 0,
            "sports": 0,
            "music": 0,
            "volunteering": 0,
            "parental_education": 2,
        },
        "🔴 Perfil de Risco — baixa dedicação, muitas faltas": {
            "idade": 17,
            "horas_estudo": 1,
            "faltas": 28,
            "apoio_pais": 0,
            "extracurricular": 0,
            "tutoring": 0,
            "sports": 0,
            "music": 0,
            "volunteering": 0,
            "parental_education": 0,
        },
    }


def monte_carlo_previsoes(n_iter: int = 1000, random_state: int = 42) -> dict:
    """
    Simulação de Monte Carlo: sorteia combinações aleatórias dentro dos
    limites reais do dataset e avalia a distribuição das previsões escaladas.
    """
    rng = np.random.default_rng(random_state)
    previsoes: list[float] = []
    for _ in range(n_iter):
        gpa = prever_gpa(
            idade              = int(rng.integers(15, 19)),
            horas_estudo       = float(rng.uniform(0, 20)),
            faltas             = int(rng.integers(0, 30)),
            apoio_pais         = int(rng.integers(0, 5)),
            extracurricular    = int(rng.integers(0, 2)),
            tutoring           = int(rng.integers(0, 2)),
            sports             = int(rng.integers(0, 2)),
            music              = int(rng.integers(0, 2)),
            volunteering       = int(rng.integers(0, 2)),
            parental_education = int(rng.integers(0, 5)),
        )
        previsoes.append(gpa)

    arr = np.array(previsoes)
    return {
        "previsoes": arr,
        "media":  float(arr.mean()),
        "desvio": float(arr.std()),
        "min":    float(arr.min()),
        "max":    float(arr.max()),
        "p5":     float(np.percentile(arr, 5)),
        "p95":    float(np.percentile(arr, 95)),
    }