import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração inicial do título da janela
def configure_page():
    st.set_page_config(page_title="Indicadores referente ao arquivo CSV", page_icon="👁")

# Carrega o arquivo CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Processa dados de contagem por gênero
def get_gender_counts(data):
    gender_counts = data['gender'].value_counts().rename_axis('gender').reset_index(name='counts')
    gender_counts.set_index('gender', inplace=True)
    return gender_counts

# Processa dados de contagem por geração
def get_generation_counts(data):
    generation_counts = data['generation'].value_counts().rename_axis('generation').reset_index(name='counts')
    generation_counts.set_index('generation', inplace=True)
    return generation_counts

# Calcula a média de anos de educação por gênero
def get_gender_education_mean(data):
    gender_education_mean = data.groupby('gender')['years_of_education'].mean().reset_index(name='means')
    gender_education_mean.set_index('gender', inplace=True)
    return gender_education_mean

# Processa dados de contagem de status de emprego
def get_job_counts(data):
    job_counts = data['employment_status'].value_counts().rename_axis('employment_status').reset_index(name='counts')
    job_counts.set_index('employment_status', inplace=True)
    return job_counts

# Cria faixas de idade e retorna distribuição por idade
def get_age_group_counts(data):
    data['age_group'] = pd.cut(data['age'], bins=[0, 18, 30, 45, 60, 100], labels=['0-18', '19-30', '31-45', '46-60', '61+'])
    age_group_counts = data['age_group'].value_counts().sort_index()
    return age_group_counts

# Retorna a distribuição de idade por gênero
def get_age_gender_distribution(data):
    age_gender_distribution = data.groupby(['age_group', 'gender'], observed=True).size().unstack(fill_value=0)
    return age_gender_distribution

# Exibe gráficos e dados no Streamlit
def display_dashboard(data):
    st.title("Indicadores referente ao arquivo CSV")
    st.subheader("Dados de origem")
    st.dataframe(data)

    # Gráfico do número de pessoas por gênero
    st.divider()
    st.subheader("Número de pessoas por gênero")
    gender_counts = get_gender_counts(data)
    st.bar_chart(gender_counts['counts'], x_label="Gêneros", y_label="Quantidade")

    # Gráfico do número de pessoas por geração
    st.divider()
    st.subheader("Número de pessoas por geração")
    generation_counts = get_generation_counts(data)
    st.bar_chart(generation_counts['counts'], color="#ffaa00", x_label="Geração", y_label="Quantidade", horizontal=True)

    # Gráfico da média de anos trabalhados
    st.divider()
    st.subheader("Média de anos trabalhados")
    gender_education_mean = get_gender_education_mean(data)
    st.bar_chart(gender_education_mean['means'], color="#00aa00", x_label="Gênero", y_label="Média de anos trabalhados")

    # Gráfico de pizza do Status de Emprego
    st.divider()
    st.subheader("Distribuição do Status de Emprego")
    job_counts = get_job_counts(data)
    fig_job_status = px.pie(job_counts, values='counts', names=job_counts.index)
    st.plotly_chart(fig_job_status)

    # Histograma geral de idades
    st.divider()
    st.subheader("Distribuição por Idade")
    age_group_counts = get_age_group_counts(data)
    fig_age_group = px.bar(age_group_counts, labels={"value": "Número de Pessoas", "variable": "Idade"}, barmode='stack')
    fig_age_group.update_layout(xaxis_title="Idades")
    st.plotly_chart(fig_age_group)

    # Histograma de idades por gênero
    st.divider()
    st.subheader("Distribuição por Idade e Gênero")
    age_gender_distribution = get_age_gender_distribution(data)
    fig_age_gender = px.bar(age_gender_distribution, labels={"value": "Número de Pessoas", "variable": "Idade"}, barmode='group')
    fig_age_gender.update_layout(xaxis_title="Idades")
    st.plotly_chart(fig_age_gender)

# Função principal
def main():
    configure_page()
    file_path = 'persons.csv'
    data = load_data(file_path)
    display_dashboard(data)

if __name__ == "__main__":
    main()
