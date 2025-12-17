import pickle
from io import BufferedWriter

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def main():

    # Importando um conjunto de dados com informações de saúde e hábitos de mais de 2.000 pacientes.
    df_main = pd.read_csv('../files/obesity.csv')

    print(f'\n{100 * "*"}\nAmostra de dados (sample)\n{100 * "*"}')
    print(df_main.sample(5))

    print(f'\n{100 * "*"}\nDimensões: Linhas e Colunas (shape)\n{100 * "*"}')
    print(df_main.shape)

    print(f'\n{100 * "*"}\nEstrutura: Tipos de dados (info)\n{100 * "*"}')
    print(df_main.info())

    print(f'\n{100 * "*"}\nResumo estátistico (describe)\n{100 * "*"}')
    print(df_main.describe())

    # Garantindo a qualidade dos dados:
    # Aqui verificamos se há dados faltando (nulos) ou informações repetidas (duplicados)
    print(f'\n{100 * "*"}\nValores nulos e/ou duplicados\n{100 * "*"}')
    print(df_main[df_main.isnull().any(axis=1)])
    print(df_main.duplicated().sum())

    # Engenharia de recursos: transformar dados brutos em insights valiosos.
    # Aqui calculamos o IMC (BMI), um dos indicadores mais poderosos para prever a obesidade.
    df_main['BMI'] = df_main['Weight'] / (df_main['Height'] ** 2)

    # Aqui separamos nossos dados em 'features numéricas' (idade, peso) e 'features categóricas' (gênero, consumo de álcool)
    # As features numéricas o modelo entende diretamete e as features categóricas precisam de um tratamento especial antes de entrar no modelo.
    categorical_features = ['Gender', 'CALC']
    numeric_features = ['Age', 'Height', 'Weight', 'BMI']

    # O 'X' são as características (as perguntas do teste), e o 'y' é o rótulo (o gabarito).
    # Aqui o objetivo é treinar um modelo que aprenda a mapear X para y.
    X = df_main.drop('Obesity', axis=1)
    y = df_main['Obesity']

    # Aqui nós precisamos garantir que todos os dados estarão no formato numérico que o modelo espera.
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
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='drop'
    )

    # Aqui temos a etapa mais crucial para um teste justo. Dividimos os dados em dois grupos:
    # um para 'treinar' o modelo e outro, completamente separado, para 'testar' sua performance.
    # random_state=42` garante que essa divisão seja sempre a mesma, para que os resultados sejam reproduzíveis.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Automatização do processo em um Pipeline que funciona como uma linha de montagem:
    # Os dados entram brutos, passam pelo preprocessor e são entregues prontos para o classifier treinar ou prever.
    # O uso do Pipeline garante que você aplique as mesmas transformações nos dados de treino e de teste,
    # evitando um erro muito comum chamado data leakage (vazamento de dados)
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    # Aqui alimentamos a linha de montagem com os dados de treino.
    # O Pipeline executa a preparação e o RandomForest aprende os padrões que ligam
    # os dados do paciente ao seu nível de obesidade.
    # Funciona da seguinte forma:
    # O Pipeline pega X_train e o envia para a primeira estação, o preprocessor.
    # O preprocessor transforma X_train em um array numérico.
    # O Pipeline pega esse array numérico e o entrega, junto com y_train, para a segunda estação, o classifier.
    # O classifier então usa esses dados para treinar.
    model.fit(X_train, y_train)

    # Aqui são usados os dados de teste (que ele nunca viu antes) para fazer a avaliação de desempenho do modelo treinado.
    # O Pipeline garante que os dados de teste passem pela MESMA preparação.
    y_pred = model.predict(X_test)

    # Calcular a precisão:
    # Aqui medimos a acurácia do modelo. Qual a porcentagem de acertos do modelo no teste cego?
    accuracy = accuracy_score(y_test, y_pred)
    print(f'\n{100 * "*"}\nPrecisão do modelo\n{100 * "*"}')
    print(f'{accuracy:.4f}')

    # Relatório de Classificação:
    # Uma amostra mais detalhada do desempenho do modelo, mostrando o desempenho para cada categoria de obesidade.
    print(f'\n{100 * "*"}\nAmostra de desempenho do modelo\n{100 * "*"}')
    print(classification_report(y_test, y_pred))

    # Aqui 'Engarrafamos' toda a inteligência do modelo treinado em um único arquivo.
    # Agora, qualquer outra aplicação pode carregar este arquivo e usar o modelo pronto, sem precisar treinar novamente.
    file: BufferedWriter
    with open('../files/obesity_model.pkl', 'wb') as file:
        pickle.dump(model, file)

    print("\n** Modelo treinado e salvo com sucesso como obesity_model.pkl **")

if __name__ == '__main__':
    main()
