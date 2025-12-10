import streamlit as st
import pandas as pd
import pickle

# Dicionários para tradução e informação adicional
traducao_niveis = {
    "Insufficient_Weight": "Peso Insuficiente",
    "Normal_Weight": "Peso Normal",
    "Overweight_Level_I": "Sobrepeso Nível I",
    "Overweight_Level_II": "Sobrepeso Nível II",
    "Obesity_Type_I": "Obesidade Tipo I",
    "Obesity_Type_II": "Obesidade Tipo II",
    "Obesity_Type_III": "Obesidade Tipo III"
}

info_niveis = {
    "Peso Insuficiente": "Atenção: Seu peso está abaixo do ideal. É recomendável procurar um médico ou nutricionista para avaliação.",
    "Peso Normal": "Parabéns! Seu peso está na faixa considerada normal. Continue mantendo um estilo de vida saudável.",
    "Sobrepeso Nível I": "Atenção: Você está com sobrepeso. Pequenas mudanças na dieta e rotina de exercícios podem trazer grandes benefícios.",
    "Sobrepeso Nível II": "Cuidado: Seu quadro é de sobrepeso. É aconselhável buscar orientação médica para evitar a progressão para obesidade.",
    "Obesidade Tipo I": "Alerta: Seu quadro é de Obesidade Grau I. É fundamental procurar acompanhamento médico para desenvolver um plano de saúde.",
    "Obesidade Tipo II": "Alerta de Saúde: Seu quadro é de Obesidade Grau II. O acompanhamento com uma equipe de saúde é crucial para reverter o quadro.",
    "Obesidade Tipo III": "Alerta Crítico de Saúde: Seu quadro é de Obesidade Grau III (mórbida). Procure ajuda médica imediatamente."
}


# Título da aplicação
st.title('Preditor de Nível de Obesidade')
st.write('Insira os dados abaixo para prever o nível de obesidade.')

# 1. Carregar modelo
try:
    with open('src/obesity_model.pkl', 'rb') as f:
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
    # Criar um DataFrame com TODAS as colunas esperadas pelo modelo
    data = {
        'Gender': [gender],
        'Age': [age],
        'Height': [height],
        'Weight': [weight],
        'family_history': ['yes'], # Valor padrão
        'FAVC': ['yes'],           # Valor padrão
        'FCVC': [2.0],             # Valor padrão
        'NCP': [3.0],              # Valor padrão
        'CAEC': ['Sometimes'],     # Valor padrão
        'SMOKE': ['no'],           # Valor padrão
        'CH2O': [2.0],             # Valor padrão
        'SCC': ['no'],             # Valor padrão
        'FAF': [0.0],              # Valor padrão
        'TUE': [1.0],              # Valor padrão
        'CALC': [calc],
        'MTRANS': ['Public_Transportation'] # Valor padrão
    }
    input_df = pd.DataFrame(data)

    # 4. Calcular o BMI (Índice de Massa Corporal)
    input_df['BMI'] = input_df['Weight'] / (input_df['Height'] ** 2)

    # 5. Fazer a predição
    prediction = model.predict(input_df)[0]
    
    # 6. Traduzir e obter informação adicional
    resultado_traduzido = traducao_niveis.get(prediction, "Categoria Desconhecida")
    info_adicional = info_niveis.get(resultado_traduzido, "Não há informações adicionais para esta categoria.")

    # 7. Exibir o resultado
    st.subheader('Resultado da Predição:')
    st.write(f'O paciente se enquadra na categoria: **{resultado_traduzido}**')
    
    # Exibir a informação adicional com um estilo de alerta
    if "Alerta Crítico" in info_adicional or "Alerta de Saúde" in info_adicional:
        st.error(info_adicional)
    elif "Alerta" in info_adicional or "Cuidado" in info_adicional or "Atenção" in info_adicional:
        st.warning(info_adicional)
    else:
        st.success(info_adicional)
