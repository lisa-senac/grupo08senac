import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

_URL = (
    "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/"
    "Student_performance_data.xlsx"
)

_COLS_X = [
    "Age",
    "StudyTimeWeekly",
    "Absences",
    "ParentalSupport",
    "Extracurricular",
    "Tutoring",
    "Sports",
    "Music",
    "Volunteering",
    "ParentalEducation",
]

df = pd.read_excel(_URL)

X = df[_COLS_X].copy()
y = df["GPA"].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
r2 = r2_score(y_test, y_pred)


def _parear_rotulos_valores(rotulos, valores):
    vals = sorted(int(v) for v in valores)
    labs = list(rotulos)
    while len(labs) < len(vals):
        labs.append(f"Categoria {len(labs) + 1}")
    return list(zip(labs[: len(vals)], vals))


_SUP_VALS = sorted(X["ParentalSupport"].astype(int).unique().tolist())
_EDU_VALS = sorted(X["ParentalEducation"].astype(int).unique().tolist())

# A base usa ParentalSupport em escala ordinal 0–4 (cinco níveis).
_ROTULOS_APOIO = [
    "Muito baixo",
    "Baixo",
    "Médio",
    "Alto",
    "Muito alto",
]
_ROTULOS_EDU = [
    "Nenhuma",
    "Ensino Fundamental",
    "Ensino Médio",
    "Faculdade",
    "Pós-graduação",
]

OPCOES_APOIO_FAMILIAR = _parear_rotulos_valores(_ROTULOS_APOIO, _SUP_VALS)
OPCOES_ESCOLARIDADE_PAIS = _parear_rotulos_valores(_ROTULOS_EDU, _EDU_VALS)

_Q1, _Q3 = y.quantile([0.33, 0.66]).tolist()


def metricas_validacao():
    """MAE, RMSE e R² no conjunto de teste (hold-out 20%)."""
    return {"mae": float(mae), "rmse": rmse, "r2": float(r2)}


def classificar_potencial_academico(gpa_previsto):
    """
    Interpretação qualitativa em três faixas, calibradas pela distribuição
    do GPA na base de treinamento (tercis empíricos).
    """
    g = float(gpa_previsto)
    if g < _Q1:
        return (
            "Potencial de ingresso em instituição de ensino superior de perfil mediano.",
            "error",
        )
    if g < _Q3:
        return (
            "Potencial de ingresso em instituição de ensino superior de bom nível.",
            "warning",
        )
    return (
        "Potencial de ingresso em instituição de ensino superior de alta competitividade.",
        "success",
    )


def _entrada_dataframe(
    idade,
    horas_estudo,
    faltas,
    apoio_pais,
    extracurricular,
    tutoring,
    sports,
    music,
    volunteering,
    parental_education,
):
    return pd.DataFrame(
        [
            {
                "Age": idade,
                "StudyTimeWeekly": horas_estudo,
                "Absences": faltas,
                "ParentalSupport": int(apoio_pais),
                "Extracurricular": int(extracurricular),
                "Tutoring": int(tutoring),
                "Sports": int(sports),
                "Music": int(music),
                "Volunteering": int(volunteering),
                "ParentalEducation": int(parental_education),
            }
        ]
    )


def prever_gpa(
    idade,
    horas_estudo,
    faltas,
    apoio_pais,
    extracurricular,
    tutoring,
    sports,
    music,
    volunteering,
    parental_education,
):
    """Regressão linear treinada nas colunas de _COLS_X."""
    entrada = _entrada_dataframe(
        idade,
        horas_estudo,
        faltas,
        apoio_pais,
        extracurricular,
        tutoring,
        sports,
        music,
        volunteering,
        parental_education,
    )
    return float(modelo.predict(entrada)[0])


def cenarios_stress():
    """
    Combinações extremas e intermediárias dentro dos limites observados na base.
    """
    lo = X.min(numeric_only=True)
    hi = X.max(numeric_only=True)
    mid = X.mean(numeric_only=True)

    def pack(row):
        return {
            "idade": int(round(row["Age"])),
            "horas_estudo": float(row["StudyTimeWeekly"]),
            "faltas": int(round(row["Absences"])),
            "apoio": int(round(row["ParentalSupport"])),
            "extracurricular": int(round(row["Extracurricular"])),
            "tutoring": int(round(row["Tutoring"])),
            "sports": int(round(row["Sports"])),
            "music": int(round(row["Music"])),
            "volunteering": int(round(row["Volunteering"])),
            "parental_education": int(round(row["ParentalEducation"])),
        }

    excelente = pack(
        pd.Series(
            {
                "Age": hi["Age"],
                "StudyTimeWeekly": hi["StudyTimeWeekly"],
                "Absences": lo["Absences"],
                "ParentalSupport": hi["ParentalSupport"],
                "Extracurricular": hi["Extracurricular"],
                "Tutoring": hi["Tutoring"],
                "Sports": hi["Sports"],
                "Music": hi["Music"],
                "Volunteering": hi["Volunteering"],
                "ParentalEducation": hi["ParentalEducation"],
            }
        )
    )

    risco = pack(
        pd.Series(
            {
                "Age": lo["Age"],
                "StudyTimeWeekly": lo["StudyTimeWeekly"],
                "Absences": hi["Absences"],
                "ParentalSupport": lo["ParentalSupport"],
                "Extracurricular": lo["Extracurricular"],
                "Tutoring": lo["Tutoring"],
                "Sports": lo["Sports"],
                "Music": lo["Music"],
                "Volunteering": lo["Volunteering"],
                "ParentalEducation": lo["ParentalEducation"],
            }
        )
    )

    intermediario = pack(mid)
    return {
        "Cenário 1 — elevada dedicação aos estudos e baixa incidência de faltas "
        "(combinação otimista nos limites da base)": excelente,
        "Cenário 2 — desempenho acadêmico intermediário (valores médios da base)": intermediario,
        "Cenário 3 — baixa dedicação aos estudos e elevado número de ausências "
        "(combinação pessimista nos limites da base)": risco,
    }


def prever_gpa_dict(c):
    return prever_gpa(
        c["idade"],
        c["horas_estudo"],
        c["faltas"],
        c["apoio"],
        c["extracurricular"],
        c["tutoring"],
        c["sports"],
        c["music"],
        c["volunteering"],
        c["parental_education"],
    )


def monte_carlo_previsoes(n_iter=800, random_state=42):
    """
    Amostragem uniforme por variável entre min e max da base (0/1 para binárias).
    Retorna estatísticas das previsões para avaliar consistência / dispersão.
    """
    rng = np.random.default_rng(random_state)
    preds = np.empty(n_iter, dtype=float)
    for i in range(n_iter):
        row = {}
        for col in _COLS_X:
            s = X[col]
            vmin, vmax = float(s.min()), float(s.max())
            if s.dropna().astype(int).nunique() <= 2:
                row[col] = int(rng.integers(0, 2))
            else:
                row[col] = float(rng.uniform(vmin, vmax))
        entrada = pd.DataFrame([row])[_COLS_X]
        preds[i] = modelo.predict(entrada)[0]
    return {
        "previsoes": preds,
        "media": float(np.mean(preds)),
        "desvio": float(np.std(preds)),
        "min": float(np.min(preds)),
        "max": float(np.max(preds)),
        "p5": float(np.percentile(preds, 5)),
        "p95": float(np.percentile(preds, 95)),
    }


def coeficientes_ordenados():
    out = pd.DataFrame({"Variável": _COLS_X, "Coeficiente": modelo.coef_})
    out["|Coeficiente|"] = out["Coeficiente"].abs()
    return out.sort_values("|Coeficiente|", ascending=False)


if __name__ == "__main__":
    m = metricas_validacao()
    print("\n=== MÉTRICAS DO MODELO (teste) ===")
    print(f"MAE  : {m['mae']:.4f}")
    print(f"RMSE : {m['rmse']:.4f}")
    print(f"R²   : {m['r2']:.4f}")
    print("\n=== Coeficientes (|valor|) ===")
    print(coeficientes_ordenados().to_string(index=False))
