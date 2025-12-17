import pickle
import pandas as pd
from flask import Flask, request, jsonify

# Iniciar a aplicação Flask
app = Flask(__name__)

# --- Carregar o modelo salvo ---
try:
    with open('../files/obesity_model.pkl', 'rb') as file:
        model = pickle.load(file)
    print("Modelo carregado com sucesso!")
except FileNotFoundError:
    print("Erro: obesity_model.pkl não encontrado. Certifique-se de que o script de treinamento foi executado.")
    model = None


# --- Definir a rota para a predição ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Modelo não carregado'}), 500

    try:
        # Receber os dados do cliente
        data = request.json

        # Criar um DataFrame com os dados recebidos.
        # As chaves do JSON devem corresponder às colunas usadas no treinamento.
        input_df = pd.DataFrame([data])
        # Calcular o BMI no servidor
        if 'Height' in input_df.columns and 'Weight' in input_df.columns:
            input_df['BMI'] = input_df['Weight'] / (input_df['Height'] ** 2)
        else:
            return jsonify({'error': 'Peso e altura são necessários para calcular o BMI.'}), 400

        # Realizar a predição
        prediction = model.predict(input_df)

        # Retornar a predição como JSON
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # Iniciar o servidor web
    app.run(debug=True)
