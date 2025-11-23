import streamlit as st

st.set_page_config(
    page_title="Análise de Obesidade",
    page_icon="🩺",
    layout="wide"
)

st.title("Plataforma de Análise de Fatores de Risco para Obesidade")

st.markdown("""
### Bem-vindo à plataforma de análise de obesidade!

Esta ferramenta foi desenvolvida para fornecer insights valiosos à equipe médica e permitir consultas preditivas sobre os níveis de obesidade com base em dados de pacientes.

**Use a barra de navegação à esquerda para acessar as diferentes seções:**

- **Consulta Individual:** Uma ferramenta para prever o nível de obesidade de um único paciente com base em suas informações.
- **Painel Analítico:** Uma visão interativa e agregada dos dados, destacando as correlações e os fatores mais importantes relacionados à obesidade.

Este projeto utiliza um modelo de Machine Learning treinado com dados de pacientes para fornecer as predições e os insights.
""")

st.sidebar.success("Selecione uma página acima.")