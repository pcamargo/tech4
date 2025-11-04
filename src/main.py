import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

def main():
    df_main = pd.read_csv('../files/obesity.csv')
    #print(df_main.info())
    #print(df_main.head())

    #pd.set_option('display.max_columns', None)
    #print(df_main.sample(5))

    print('\nValores nulos')
    print(df_main.isnull().sum())

    print('\nValores duplicados:')
    print(df_main.duplicated().sum())

    print('\nEngenharia de recursos: Calcular o IMC')
    df_main['BMI'] = df_main['Weight'] / (df_main['Height'] ** 2)

    print('\nDefinir colunas categóricas e numéricas')
    categorical_features = ['Gender', 'CALC']
    numeric_features = ['Age', 'Height', 'Weight', 'BMI']

    #df_main = pd.get_dummies(df_main, columns=['Gender', 'CALC'])
    #print(df_main.head())

    print('\nSeparar recursos (X) e rótulo (y)')
    X = df_main.drop('Obesity', axis=1)
    y = df_main['Obesity']

    print(X.head())
    print(y.head())

    # Modelos de machine learning são baseados em matemática e não entendem texto como "Male" ou "Sometimes".
    # Por isso, precisamos converter essas categorias em números e é aqui que entra o One-Hot Encoding
    # O que entra? O DataFrame X bruto.
    # O que acontece? O ColumnTransformer (que você chamou de preprocessor) faz:
    # Pega as colunas numéricas e deixa passar.
    # Pega as colunas categóricas e as transforma em colunas de 0s e 1s (OneHotEncoder).
    # Joga fora o resto das colunas.
    # O que sai? Uma nova tabela, agora totalmente numérica.
    # O resultado é um array NumPy.
    # O Scikit-learn prefere usar arrays NumPy por baixo dos panos por serem mais eficientes para cálculos matemáticos.
    # Aplicar técnica One-Hot Encoding
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='drop'
    )

    print('\nModelagem preditiva')
    print('Dividir os dados em treino e teste')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # O uso do Pipeline garante que você aplique as mesmas transformações nos dados de treino e de teste,
    # evitando um erro muito comum chamado data leakage (vazamento de dados)
    print('Criar o pipeline com pré-processamento e modelo')
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    # O Pipeline pega X_train e o envia para a primeira estação, o preprocessor.
    # O preprocessor transforma X_train em um array numérico.
    # O Pipeline pega esse array numérico e o entrega, junto com y_train, para a segunda estação, o classifier.
    # O classifier então usa esses dados para treinar.
    print('\nTreinar o modelo')
    model.fit(X_train, y_train)

    # O Pipeline pega X_test e o envia para a primeira estação, o preprocessor.
    # O preprocessor aplica exatamente as mesmas transformações que aprendeu com os dados de treino.
    # O Pipeline pega o array numérico resultante e o entrega para a segunda estação, o classifier.
    # O classifier usa o array para fazer as previsões
    print('\nFazer previsões')
    y_pred = model.predict(X_test)

    # 3. Avaliar o modelo
    # Calcular a precisão
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Precisão do modelo: {accuracy:.4f}')

    # Relatório de classificação
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred))

    print('\nSalvar o modelo treinado com pickle')
    with open('obesity_model.pkl', 'wb') as file:
        pickle.dump(model, file)

    print("Modelo treinado e salvo com sucesso como obesity_model.pkl")

if __name__ == '__main__':
    main()
