# grupo08
**Tema do Projeto** : 
Modelo preditivo da nota de um aluno do ensino médio baseado nas variáveis disponíveis em base de dados e se existe probabilidade da pessoa passar ou não em uma faculdade mediana, boa ou excelente. O GPA será a variável dependente adaptada ou traduzida como "Desempenho Escolar Geral" para o contexto brasileiro.

**Integrantes :**
Jadson Algeri Demetrio
Jefferson Lourenco dos Santos
Lisa Mari Nakakuki Meireles
Erick Massahiro Yamamoto
Edson Miranda Pimenta Junior
Matheus Santos Cruz 
Yuri Miranda Nunes 

**Planejamento de tarefas :**

Erick Massahiro Yamamoto  - Descrever brevemente o contexto da concorrência para o ensino superior no Brasil, ampliação possibilidade para ingressar na faculdade através de programas federais como Prouni e SISU tendo como consequente necessidade de se preparar previamente para atingir uma boa nota no ENEM (equivalente ao GPA)

Lisa Mari Nakakuki Meireles - Descrever objetivo, tipo de problema, metodologia de análise de dados, processamento dos dados, requisitos dos modelos de dados, futuras melhorias no modelo

Edson Miranda Pimenta Junior - Como os dados brutos serão preparados antes de treinar o modelo: descrever estudos que serão necessários realizar antes de definir uma fórmula preditiva de GPA, tais como: regressão linear, peso das variáveis, interação das variáveis (exemplo: quanto mais horas de estudo maior o GPA?)

Jefferson Lourenco dos Santos - Quais bibliotecas (Panda, Numpy, Scikit-learn) utilizar para cada cálculo (exemplo: Numpy para cálculo de correlação)

Jadson Algeri Demetrio  - Como será definido a fórmula preditiva: quais fatores não influenciam no modelo e quais variáveis que serão utilizadas

Yuri Miranda Nunes - De que forma serão feitos os testes “stress tests” , descrever como atestar a confiabilidade do modelo, avaliação da sensibilidade da variação dos dados (horas de estudo, idade, gênero, faltas etc)

Matheus Santos Cruz - Ideia inicial do dashboard  e  quais visualizações e métricas desejamos apresentar no dashboard.

============================================================================================

**Introdução**

O ensino superior no Brasil passou por uma grande transformação nos últimos anos, principalmente em termos quantitativos. Nesse período, presenciamos um crescimento de 300% nas matrículas, visto que os números saltaram de 2,1 milhões para 8,4 milhões entre 1998 e 2018. Consequentemente, a concorrência tornou-se extremamente acirrada para o ingresso nas faculdades públicas de referência nacional. Por exemplo, o curso de Medicina chegou a uma nota de corte de 820,60 na Universidade Federal de Santa Catarina (UFSC).

O crescimento no número de ingressos nas faculdades pelo Brasil foi influenciado pelo surgimento de programas como o ProUni e o Sisu, que utilizam o Exame Nacional do Ensino Médio (Enem) como critério central. 

O Sistema de Seleção Unificada (Sisu) possibilitou a unificação das ofertas em instituições públicas, permitindo que os candidatos concorram a vagas em diversas regiões por meio da média ponderada de seus resultados no Enem.
Já o Programa Universidade para Todos (ProUni) democratiza o acesso a faculdades privadas através de bolsas integrais e parciais, favorecendo estudantes de baixa renda e egressos da rede pública. 

Devido à alta competitividade e seletividade, surge a necessidade de uma preparação prévia e estratégica para permitir que os candidatos atinjam as notas necessárias. Para alcançar as notas de corte, os estudantes precisam dominar conhecimentos interdisciplinares, técnicas de redação e gestão de tempo. Como resultado, o planejamento acadêmico torna-se um diferencial decisivo para converter o esforço de estudo em uma vaga nas instituições mais concorridas do sistema.

**Objetivo da Análise:**
Determinar quais variáveis realmente influenciam na aprovação de um aluno, correlação  e se existe alguma forma de compensar a deficiência entre elas.

**Metodologia de análise e processamento de dados :**  
Na primeira etapa, será feita uma análise descritiva tomando como base de dados do repositório público Kaggle no link : https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset .  Na segunda etapa, será efetuado o pré- processamento dos dados para entender e corrigir as inconsistências e ausência de dados e identificar outliers. Teremos, por fim, um panorama apresentado em dashboard do perfil e variáveis que influenciam no desempenho dos alunos e poderemos partir para a análise preditiva, definindo assim o modelo estatístico que será capaz de prever o resultado do aluno definido em objetivo do Projeto. 

**Requisitos de Qualidade e Estrutura da Base de Dados :**  Possíveis auditorias periódicas via amostragem poderão ser necessárias para avaliar a consistência dos dados, atualidade e precisão. 

**Definição da Fórmula Preditiva do GPA** 
Nesta etapa do projeto, será definida a fórmula preditiva do desempenho acadêmico (GPA), com base na identificação das variáveis mais relevantes presentes na base de dados dos estudantes. O objetivo é construir um modelo capaz de estimar o GPA a partir de fatores que realmente influenciam o rendimento acadêmico, garantindo maior precisão e confiabilidade nas previsões.

Inicialmente, será realizada uma análise exploratória dos dados, buscando compreender o comportamento das variáveis disponíveis, suas distribuições e possíveis relações com o GPA. Essa análise permitirá identificar padrões e tendências, além de auxiliar na detecção de variáveis com maior potencial explicativo.

A partir disso, serão avaliadas as correlações entre as variáveis independentes e o desempenho acadêmico, utilizando métricas estatísticas apropriadas. Variáveis que apresentarem maior relação com o GPA serão consideradas para compor o modelo preditivo. Entre os principais fatores analisados, destacam-se horas de estudo, frequência às aulas, número de faltas, participação em atividades extracurriculares e influência dos pais, uma vez que esses elementos estão diretamente associados ao comportamento acadêmico dos estudantes.

Por outro lado, variáveis que não apresentarem impacto significativo no desempenho poderão ser descartadas do modelo. Fatores como gênero e idade, quando não demonstram correlação relevante com o GPA, tendem a não contribuir de forma significativa para a previsão e, portanto, sua inclusão pode gerar ruídos ou reduzir a eficiência do modelo.

Após a seleção das variáveis mais relevantes, será aplicada uma abordagem baseada em regressão linear múltipla, na qual o GPA será representado como uma combinação ponderada dessas variáveis. Os coeficientes atribuídos a cada fator serão definidos automaticamente durante o processo de treinamento, refletindo o grau de influência de cada variável no resultado final.

Além disso, será considerada a possibilidade de interação entre variáveis, analisando como a combinação de diferentes fatores pode impactar o desempenho acadêmico. Por exemplo, a associação entre altas horas de estudo e elevada frequência pode potencializar o GPA, enquanto a combinação de baixa dedicação aos estudos com alto número de faltas pode resultar em desempenho inferior.

Será realizada uma etapa de validação do modelo, com o objetivo de garantir que apenas variáveis relevantes sejam mantidas na fórmula preditiva. Esse processo contribui para evitar ajustes excessivos aos dados de treinamento e assegura que o modelo seja capaz de generalizar adequadamente para novos dados, mantendo sua consistência e confiabilidade.

Futuras melhorias no modelo : Ser possível medir de forma online através de coleta automática de dados e que possa complementar a precisão do modelo tais como : tempo de uso no celular, tempo de uso de redes sociais, horário que acorda e dorme etc. 

**Etapas do Processo de ETL ( Extrair, Transformar e Carregar)** - As etapas de extração e transformação dos dados para dar suporte às análises descritivas e preditivas serão executadas da seguinte forma:

1. Extração (Extract)
Utilizar Pandas para importar e organizar dados da planilha (CSV/Excel).

2. Transformação (Transform)
   
     2.1 - Uso combinado de Pandas e NumPy para limpeza e preparação dos dados por relevância (influência dos pais, atividades extracurriculares, tempo de estudo). Será realizada a limpeza dos dados, incluindo a remoção ou tratamento de valores ausentes (missing values), correção de inconsistências e padronização de formatos. Em seguida, será feito o tratamento de outliers, identificando valores extremos que possam distorcer os resultados do modelo.
  
     2.2 - Criação de novas variáveis derivadas: Será realizada a engenharia de variáveis (feature engineering), criando novas variáveis, como por exemplo a média de horas de estudo por semana , proporções ou agrupamentos, com o objetivo de melhorar o desempenho do modelo.
  
     2.3 - Cálculos matemáticos e estatísticos de correlação entre variáveis: Será analisada a interação entre variáveis, verificando como a combinação entre diferentes fatores pode afetar o resultado.Verificar a relação entre as variáveis independentes (como horas de estudo, frequência, idade, entre outras) e a variável dependente (GPA). Por exemplo, será investigado se o aumento das horas de estudo está diretamente relacionado a um maior GPA, ou se essa relação depende de outras variáveis, como frequência escolar ou condições socioeconômicas.
   
      Será conduzida uma Análise Exploratória de Dados (EDA), com o intuito de compreender a distribuição das variáveis e identificar padrões iniciais. Nessa fase, serão utilizadas estatísticas descritivas e medidas de correlação para verificar a relação entre as variáveis independentes (como horas de estudo, frequência, idade, entre outras) e a variável dependente (GPA).

      Um dos principais estudos aplicados será a regressão linear, que permitirá avaliar a relação entre as variáveis e estimar o impacto individual de cada uma no desempenho acadêmico. Esse processo ajuda a identificar o peso das variáveis, ou seja, quais fatores possuem maior influência na previsão do GPA.
  
     2.4 - Normalização de valores numéricos para padronizar escalas. Os dados serão preparados para o treinamento por meio de técnicas como normalização ou padronização, garantindo que todas as variáveis estejam na mesma escala, o que é essencial para o bom funcionamento de algoritmos de machine learning.
  
     2.5 - Pré-processamento (Scikit-Learn) :
  
   Divisão dos dados em treino e teste - Nesta etapa do projeto, os testes de estresse serão utilizados para avaliar a confiabilidade do modelo preditivo, garantindo que as previsões de desempenho acadêmico (GPA) estejam alinhadas com os padrões identificados na base de dados de estudantes.

   Treinamento de regressão linear para prever GPA - Após o treinamento do modelo de regressão linear, com dados tratados no processo de ETL, será realizada a validação por meio da divisão entre dados de treino e teste. Essa abordagem permite verificar a capacidade de generalização do modelo, evitando ajustes excessivos aos dados de treinamento.

   Avaliação do modelo com métricas (R², RMSE) - Para mensurar o desempenho, serão utilizadas métricas como erro absoluto médio (MAE), raiz do erro quadrático médio (RMSE) e coeficiente de determinação (R²), que indicam a precisão das previsões e a capacidade do modelo em explicar a variação dos dados. 

   Teste de sensibilidade e "stress test" - Na sequência, serão realizados testes de estresse com base nas principais variáveis do projeto, como horas de estudo, frequência, influência dos pais, atividades extracurriculares e número de faltas, simulando diferentes cenários para avaliar seu comportamento.

   Na prática, serão analisadas situações como: alunos com baixa carga de estudo e alta taxa de faltas; alunos com alta dedicação aos estudos e frequência elevada; e variações intermediárias entre esses cenários.

   Além disso, poderá ser utilizada uma abordagem baseada em simulação de Monte Carlo, na qual serão geradas múltiplas combinações aleatórias das variáveis de entrada, respeitando limites previamente definidos. Essa técnica permite testar o modelo em larga escala, avaliando a consistência das previsões e identificando possíveis comportamentos instáveis em cenários não observados diretamente na base original.

   Também serão definidos filtros e critérios de validação para restringir a entrada de dados a valores plausíveis, garantindo que o modelo opere em condições realistas e evitando distorções nos resultados.
  
   Espera-se que o modelo apresente comportamento estável e coerente, contribuindo para a compreensão dos fatores que influenciam o desempenho acadêmico. Ressalta-se que a precisão das previsões depende da qualidade e representatividade da base de dados utilizada.
    
4. Carga (Load)
  O dado transformado e trabalhado é enviado para um repositório centralizado a principio poderá ser utilizado o Azure SQL Database ( Plataforma baseada em SQL Server da Microsoft) que integrará os dados.


**Dashboard interativo utilizando o Streamlit**

A ideia inicial do Dashboard é consolidar os resultados da análise estatística e do modelo preditivo em um Sumário Visual Executivo.
Entregaremos um painel de visualização via Streamlit, que será gerado a partir das bibliotecas de visualização do Python como Matplotlib ou Seaborn, utilizando as métricas à seguir:

Métricas Principais (KPIs)
O painel apresentará indicadores resumidos para fornecer um contexto imediato:
-	Média Geral de GPA (Nota): O desempenho médio da base de dados analisada.
-	Taxa de Engajamento: Percentual de alunos que realizam atividades extracurriculares.
-	Índice de Correlação: Um valor que indica a força da relação entre "Horas de Estudo" e "Nota Final".

Visualizações de Dados Estratégicas
Para explicar o comportamento dos alunos e validar o modelo, utilizaremos:
-	Gráfico de Dispersão (Scatter Plot): Demonstração visual da relação direta entre horas de estudo e notas, comprovando a tendência de crescimento.
-	Gráfico de Barras Comparativo: Comparação das notas médias segmentadas por "Nível de Influência dos Pais" e "Presença de Atividades Extracurriculares".
-	Gráfico de Importância de Variáveis: Um ranking visual mostrando quais fatores (estudo, faltas ou pais) mais impactaram a previsão final do modelo.
-	Confecção de gráficos de dispersão para analisar relação entre as variáveis.
-	Heatmaps de correlação para identificar quais fatores são mais relevantes.

Matriz de Probabilidade de Aprovação
Será apresentado através de uma Tabela de Cenários (Personas). Ela detalhará as chances de ingresso em diferentes níveis de faculdade:
-	Perfil Alta Performance: (Ex: +30h de estudo + Apoio Alto) ➔ 90% de chance (Faculdade Excelente).
-	Perfil Equilibrado: (Ex: 15h de estudo + Apoio Médio) ➔ 70% de chance (Faculdade Boa).
-	Perfil de Risco: (Ex: <5h de estudo + Baixo Apoio) ➔ 30% de chance (Faculdade Mediana).




