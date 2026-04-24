import pandas as pd
url = "https://raw.githubusercontent.com/lisa-senac/grupo08senac/main/Student_performance_data.xlsx"
df = pd.read_excel(url)
print(df.head())
