import pandas as pd
url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
df = pd.read_excel(url)
print(df.head())

import pandas as pd

# carregar dados do GitHub (link raw)
url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"

df = pd.read_excel(url)

# calcular média de horas de estudo
media_estudo = df["StudyTimeWeekly"].mean()

print(end="\n\n")

# mostrar resultado
print("📊 Média de horas de estudo por semana:\n")
print(f"{media_estudo:.2f} horas")

import pandas as pd

# carregar dados
url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
df = pd.read_excel(url)

print(end="\n\n")

# mostrar antes
print("📌 Dados originais:")
print(df[["Gender", "Ethnicity", "ParentalEducation"]].head())

# aplicar One-Hot Encoding para transformar "Gender", "Ethnicity", "ParentalEducation" em cam
df_encoded = pd.get_dummies(
    df,
    columns=["Gender", "Ethnicity", "ParentalEducation"],
    drop_first=True
)
print(end="\n\n")


# mostrar depois
print("\n📊 Dados após One-Hot Encoding:")
print(df_encoded.head())

print(end="\n\n")

# mostrar colunas criadas
print("\n🧠 Novas colunas criadas:")
print(df_encoded.columns)
