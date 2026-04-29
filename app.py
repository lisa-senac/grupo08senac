import pandas as pd

#carregando dados
url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
df = pd.read_excel(url)
print(df.head())

# calcular média de horas de estudo
media_estudo = df["StudyTimeWeekly"].mean()

print(end="\n\n")

# mostrar resultado
print("Média de horas de estudo por semana:\n")
print(f"{media_estudo:.2f} horas")

print(end="\n\n")

# mostrar antes
print("Dados originais:")
print(df[["Gender", "Ethnicity", "ParentalEducation"]].head())

# aplicar One-Hot Encoding para transformar "Gender", "Ethnicity", "ParentalEducation" em cam
df_encoded = pd.get_dummies(
    df,
    columns=["Gender", "Ethnicity", "ParentalEducation"],
    drop_first=True
)
print(end="\n\n")


# mostrar depois
print("\nDados após One-Hot Encoding:")
print(df_encoded.head())

print(end="\n\n")

# mostrar colunas criadas
print("\nNovas colunas criadas:")
print(df_encoded.columns)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# definição de variáveis
y = df_encoded["GPA"]

# remover alvo e variáveis que não devem influenciar diretamente
X = df_encoded.drop(columns=["GPA", "GradeClass", "StudentID"])

# treino
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
modelo = LinearRegression()
modelo.fit(X_train, y_train)


#!=== EQUAÇÃO DE REGRESÃO ===!

intercepto = modelo.intercept_
coeficientes = modelo.coef_
variaveis = X.columns

equacao = f"GPA = {intercepto:.4f}"

for coef, var in zip(coeficientes, variaveis):
    equacao += f" + ({coef:.4f} * {var})"

print("\nEquação do modelo de regressão linear:\n")
print(equacao)


# definindo peso das variáveis
coeficientes = pd.DataFrame({
    "Variavel": X.columns,
    "Peso": modelo.coef_
})

coeficientes["Impacto"] = coeficientes["Peso"].abs()
coeficientes = coeficientes.sort_values(by="Impacto", ascending=False)

print("\nPeso das variáveis (influência no GPA):\n")
print(coeficientes[["Variavel", "Peso"]])

# avaliação do modelo
y_pred = modelo.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nAvaliação do modelo:\n")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")