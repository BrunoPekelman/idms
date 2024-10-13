import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


#configurando o titulo da janela
st.set_page_config(page_title="Indicadores referente ao grupo de pessoas", page_icon="👁")

#abre o arquivo manualmente
file = 'persons.csv'
data = pd.read_csv(file)

#parte do código responsável pelo processamento dos dados


#gerando dataset de agrupamento de genero
gender_counts = data['gender'].value_counts().rename_axis('gender').reset_index(name='counts')
gender_counts.set_index('gender', inplace=True)


#gerando dataset de agrupamento de geração
generation_counts = data['generation'].value_counts().rename_axis('generation').reset_index(name='counts')
generation_counts.set_index('generation', inplace=True)



#gerando dataset de agrupamento de média de anos de educação por gênero
gender_education_mean = data.groupby('gender')['years_of_education'].mean().reset_index(name='means')
gender_education_mean.set_index('gender', inplace=True)


#gerando dataset de estado atual de emprego
job_counts = data['employment_status'].value_counts().rename_axis('employment_status').reset_index(name='counts')
job_counts.set_index('employment_status', inplace=True)



#histograma das faixas de idade
# Criar faixas etárias
data['age_group'] = pd.cut(data['age'], bins=[0, 18, 30, 45, 60, 100], labels=['0-18', '19-30', '31-45', '46-60', '61+'])

#distribuição geral por idade
age_group_counts = data['age_group'].value_counts().sort_index()

#distribuição por gênero e por idade
age_gender_distribution = data.groupby(['age_group', 'gender'], observed=True).size().unstack(fill_value=0)



#renderizações no Streamlit
st.title("Indicadores referente ao grupo de pessoas")

st.subheader("Dados de origem")
st.dataframe(data)


#Gráfico do número de pessoas por gênero
st.divider()
st.subheader("Número de pessoas por gênero")
st.bar_chart(gender_counts['counts'], x_label="Gêneros",y_label="Quantidade")
             
#Gráfico do número de pessoas por geração (horizontal)
st.divider()
st.subheader("Número de pessoas por geração")
st.bar_chart(generation_counts['counts'], color= "#ffaa00",x_label="Geração",y_label="Quantidade", horizontal=True)

#Gráfico da média de anos trabalhados
st.divider()
st.subheader("Média de anos trabalhados")
st.bar_chart(gender_education_mean['means'], color= "#00aa00",x_label="Geração",y_label="Média de anos trabalhados")


#Gráfico de pizza do Status de Emprego no Streamlit com o Plotly
st.divider()
st.subheader("Distribuição do Status de Emprego")

fig = px.pie(job_counts, values='counts', names=job_counts.index)
st.plotly_chart(fig)



#Mostra o histograma geral de idades
st.divider()
st.subheader("Distribuição por Idade")
# Criando o gráfico de barras agrupadas
fig_grouped_age = px.bar(age_group_counts,
                     labels={"value": "Número de Pessoas", "variable": "Idade"}, 
                     barmode='stack')

fig_grouped_age.update_layout(
    xaxis_title="Idades"
)

st.plotly_chart(fig_grouped_age)



#Mostra o histograma geral de idades agrupado por gênero
st.divider()
st.subheader("Distribuição por Idade e Gênero")
# Criando o gráfico de barras agrupadas
fig_grouped_gen = px.bar(age_gender_distribution,
                     labels={"value": "Número de Pessoas", "variable": "Idade"}, 
                     barmode='group')

fig_grouped_gen.update_layout(
    xaxis_title="Idades"
)

st.plotly_chart(fig_grouped_gen)