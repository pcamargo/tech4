import streamlit as st
import pandas as pd
import pickle

# Título da aplicação
st.title('Preditor de Nível de Obesidade')
st.write('Insira os dados do paciente para prever o nível de obesidade.')

# 1. Carregar modelo
try:
    with open('obesity_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("O arquivo 'obesity_model.pkl' não foi localizado.")
    st.stop()

# 2. Criar widgets de entrada para o usuário
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox('Gênero', ['Female', 'Male'])
    age = st.number_input('Idade', min_value=1.0, max_value=100.0, value=25.0, step=1.0)
    height = st.number_input('Altura (metros)', min_value=0.5, max_value=2.5, value=1.70, step=0.01, format="%.2f")

with col2:
    weight = st.number_input('Peso (kg)', min_value=1.0, max_value=200.0, value=70.0, step=0.1, format="%.1f")
    calc = st.selectbox('Consumo de álcool', ['Sometimes', 'Frequently', 'Always', 'no'])

# Botão para fazer a predição
if st.button('Prever Nível de Obesidade'):
    # 3. Processar os dados de entrada
    # O modelo espera um DataFrame, então precisamos criar um
    data = {
        'Gender': [gender],
        'Age': [age],
        'Height': [height],
        'Weight': [weight],
        'CALC': [calc]
    }
    input_df = pd.DataFrame(data)

    # 4. Calcular o BMI (Índice de Massa Corporal)
    input_df['BMI'] = input_df['Weight'] / (input_df['Height'] ** 2)

    # 5. Fazer a predição
    prediction = model.predict(input_df)[0]

    # 6. Exibir o resultado
    st.subheader('Resultado da Predição:')
    st.write(f'O paciente se enquadra na categoria: **{prediction}**')
