import streamlit as st

st.set_page_config(
    page_title="Análise de Obesidade",
    page_icon="🩺",
    layout="wide"
)

st.title("Plataforma de Análise de Fatores de Risco para Obesidade")

st.markdown("""
### Bem-vindo à plataforma de análise de obesidade!

Esta ferramenta foi desenvolvida para fornecer insights valiosos e permitir consultas preditivas sobre os níveis de obesidade com base em dados de pacientes.
""")

st.info("""
**Use a barra de navegação à esquerda para acessar as diferentes seções:**
- **Consulta Individual:** Uma ferramenta para prever o nível de obesidade de um único paciente.
- **Painel Analítico:** Uma visão interativa dos dados, destacando correlações e fatores de risco.
""")

st.markdown("---")

st.header("Entendendo as Classificações: Sobrepeso vs. Obesidade")

st.markdown("""
A principal diferença entre **sobrepeso** (overweight) e **obesidade** é o grau de excesso de gordura corporal, medido pelo **Índice de Massa Corporal (IMC)**. A obesidade é uma condição mais grave e é, frequentemente, uma progressão do sobrepeso.

A Organização Mundial da Saúde (OMS) define as duas condições com base nos seguintes valores de IMC para adultos:
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sobrepeso")
    st.markdown("""
    - **IMC entre 25 e 29.9.**
    - Considerado o **estágio inicial** do excesso de peso.
    - Funciona como um **sinal de alerta** para a necessidade de mudanças no estilo de vida.
    """)

with col2:
    st.subheader("Obesidade")
    st.markdown("""
    - **IMC de 30 ou mais.**
    - É uma **doença crônica** caracterizada por um acúmulo excessivo e prejudicial de gordura corporal.
    - Apresenta riscos à saúde mais elevados do que o sobrepeso.
    """)

st.markdown("""
> **Nota Importante:** O cálculo do IMC é uma ferramenta prática, mas é importante notar que ela não considera a proporção de massa muscular versus gordura corporal.

**Gostaria de saber como calcular o seu próprio IMC ou entender quais são os riscos específicos associados a cada uma dessas condições?** Utilize nossa ferramenta de **Consulta Individual** no menu ao lado!
""")
