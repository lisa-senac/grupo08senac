# grupo08
Tema do Projeto : 
Modelo preditivo da nota de um aluno do ensino médio baseado nas variáveis de Hábitos de Estudo ( frequência), Influência dos pais e Atividades Extracurriculares e se existe probabilidade da pessoa passar ou não em uma faculdade mediana, boa ou excelente.

**Integrantes :**
Jadson Algeri Demetrio
Jefferson Lourenco dos Santos
Lisa Mari Nakakuki Meireles
Erick Massahiro Yamamoto
Edson Miranda Pimenta Junior
Matheus Santos Cruz 
Yuri Miranda Nunes 

**Objetivo da Análise:**
Determinar quais variáveis realmente influenciam na aprovação de um aluno, correlação  e se existe alguma forma de compensar a deficiência entre elas.

**Planejamento de tarefas :**

Erick Massahiro Yamamoto  - Descrever brevemente o contexto da concorrência para o ensino superior no Brasil, ampliação possibilidade para ingressar na faculdade através de programas federais como Prouni e SISU tendo como consequente necessidade de se preparar previamente para atingir uma boa nota no ENEM (equivalente ao GPA)

Lisa Mari Nakakuki Meireles - Descrever objetivo, tipo de problema, metodologia de análise de dados, processamento dos dados, requisitos dos modelos de dados, futuras melhorias no modelo

Edson Miranda Pimenta Junior - Como os dados brutos serão preparados antes de treinar o modelo: descrever estudos que serão necessários realizar antes de definir uma fórmula preditiva de GPA, tais como: regressão linear, peso das variáveis, interação das variáveis (exemplo: quanto mais horas de estudo maior o GPA?)

Jefferson Lourenco dos Santos - Quais bibliotecas (Panda, Numpy, Scikit-learn) utilizar para cada cálculo (exemplo: Numpy para cálculo de correlação)

Jadson Algeri Demetrio  - Como será definido a formula preditiva: quais fatores não influenciam no modelo e quais variáveis que serão utilizadas

Yuri Miranda Nunes - De que forma serão feitos os testes “stress tests” , descrever como atestar a confiabilidade do modelo, avaliação da sensibilidade da variação dos dados (horas de estudo, idade, gênero, faltas etc)

Matheus Santos Cruz - Ideia inicial do dashboard  e  quais visualizações e métricas desejamos apresentar no dashboard.

COLETIVO - Especificar o Cronograma do Projeto – Atividade final que deverá ser feito por todos do grupo

======================================================================================================================================

**Introdução**

O ensino superior no Brasil passou por uma grande transformação nos últimos anos, principalmente em termos quantitativos. Nesse período, presenciamos um crescimento de 300% nas matrículas, visto que os números saltaram de 2,1 milhões para 8,4 milhões entre 1998 e 2018. Consequentemente, a concorrência tornou-se extremamente acirrada para o ingresso nas faculdades públicas de referência nacional. Por exemplo, o curso de Medicina chegou a uma nota de corte de 820,60 na Universidade Federal de Santa Catarina (UFSC).

O crescimento no número de ingressos nas faculdades pelo Brasil foi influenciado pelo surgimento de programas como o ProUni e o Sisu, que utilizam o Exame Nacional do Ensino Médio (Enem) como critério central. 

O Sistema de Seleção Unificada (Sisu) possibilitou a unificação das ofertas em instituições públicas, permitindo que os candidatos concorram a vagas em diversas regiões por meio da média ponderada de seus resultados no Enem.
Já o Programa Universidade para Todos (ProUni) democratiza o acesso a faculdades privadas através de bolsas integrais e parciais, favorecendo estudantes de baixa renda e egressos da rede pública. 

Devido à alta competitividade e seletividade, surge a necessidade de uma preparação prévia e estratégica para permitir que os candidatos atinjam as notas necessárias. Para alcançar as notas de corte, os estudantes precisam dominar conhecimentos interdisciplinares, técnicas de redação e gestão de tempo. Como resultado, o planejamento acadêmico torna-se um diferencial decisivo para converter o esforço de estudo em uma vaga nas instituições mais concorridas do sistema.

**Metodologia de análise e processamento de dados :**  
Na primeira etapa, será feita uma análise descritiva tomando por base de dados do repositório público Kaggle no link : https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset .  Na segunda etapa, será efetuado o pré- processamento dos dados para entender e corrigir as inconsistências e ausência de dados e identificar outliers. Teremos, por fim, um panorama apresentado em dashboard do perfil e variáveis que influenciam no desempenho dos alunos e poderemos partir para a análise preditiva, definindo assim o modelo estatístico que será capaz de prever o resultado do aluno definido em objetivo do Projeto. 

**Requisitos de Qualidade e Estrutura da Base de Dados :**  Possíveis auditorias periódicas via amostragem poderão ser necessárias para avaliar a consistência dos dados, atualidade e precisão. 

Futuras melhorias no modelo : Ser possível medir de forma on-line através de coleta automática de dados de forma subsidiária que possam complementar a precisão do modelo tais como : tempo de uso no celular, tempo de uso de redes sociais, horário que acorda e dorme etc. 

**Etapas do Processo de ETL ( Extrair, Transformar e Carregar)** - As etapas de extração e transformação dos dados para dar suporte às análises descritivas e preditivas serão executadas da seguinte forma:

1. Extração (Extract)
Utilizar Pandas para importar e organizar dados da planilha (CSV/Excel).

2. Transformação (Transform)
  2.1 - Uso combinado de Pandas e NumPy para limpeza e preparação dos dados por relevância (influência dos pais, atividades extracurriculares, tempo de estudo).
  2.2 - Criação de novas variáveis derivadas (média de horas de estudo x semana).
  2.3 - Cálculos matemáticos e estatísticos de correlação entre variáveis (estudo x GPA).
  2.4 - Normalização de valores numéricos para padronizar escalas.
  2.5 - Pré-processamento (Scikit-Learn) :
   Divisão dos dados em treino e teste.
   Treinamento de regressão linear para prever GPA.
   Avaliação do modelo com métricas (R², RMSE).
   Teste de sensibilidade (influência das horas de estudos ou faltas numa possível aprovação).
   
3. Carga (Load)
  O dado transformado e trabalhado é enviado para um repositório centralizado que integrará os dados.
  Confecção de gráficos de dispersão para analisar relação entre as variáveis.
  Heatmaps de correlação para identificar quais fatores são mais relevantes.

