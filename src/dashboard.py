import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# --- Configuração da Página ---
st.set_page_config(
    page_title="Painel Analítico de Obesidade",
    page_icon="📊",
    layout="wide"
)


# --- Carregamento dos Dados ---
# Usar cache para otimizar o carregamento dos dados
@st.cache_data
def load_data():
    df = pd.read_csv('../files/obesity.csv')
    # Recalcular o IMC para garantir consistência
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)
    return df


@st.cache_data
def load_model():
    try:
        with open('obesity_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None


df = load_data()
model = load_model()

# --- Título do Painel ---
st.title("📊 Painel Analítico de Fatores de Risco para Obesidade")
st.markdown("Análise interativa dos dados de pacientes para identificar insights sobre a obesidade.")

# --- Sidebar de Filtros ---
st.sidebar.header("Filtros")
gender = st.sidebar.multiselect(
    "Filtrar por Gênero:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

family_history = st.sidebar.multiselect(
    "Filtrar por Histórico Familiar de Obesidade:",
    options=df["family_history"].unique(),
    default=df["family_history"].unique()
)

# Aplicar filtros ao dataframe
df_selection = df.query(
    "Gender == @gender & family_history == @family_history"
)

if df_selection.empty:
    st.warning("Nenhum dado disponível para os filtros selecionados. Por favor, ajuste sua seleção.")
    st.stop()

# --- Corpo do Painel ---

# 1. Visão Geral
st.header("Visão Geral da Distribuição de Obesidade")
fig_distribuicao = px.pie(
    df_selection,
    names='Obesity',
    title='Distribuição dos Níveis de Obesidade',
    hole=.3,
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig_distribuicao, use_container_width=True)

# 2. Análise Detalhada por Fatores
st.header("Análise por Fatores Demográficos e de Hábitos")
col1, col2 = st.columns(2)

with col1:
    # Idade vs. Nível de Obesidade
    fig_idade = px.box(
        df_selection,
        x='Obesity',
        y='Age',
        color='Obesity',
        title='Distribuição de Idade por Nível de Obesidade',
        labels={'Obesity': 'Nível de Obesidade', 'Age': 'Idade'}
    )
    st.plotly_chart(fig_idade, use_container_width=True)

with col2:
    # Consumo de Álcool vs. Nível de Obesidade
    fig_calc = px.histogram(
        df_selection,
        x='Obesity',
        color='CALC',
        barmode='group',
        title='Consumo de Álcool por Nível de Obesidade',
        labels={'Obesity': 'Nível de Obesidade', 'CALC': 'Consumo de Álcool'}
    )
    st.plotly_chart(fig_calc, use_container_width=True)

# 3. Relação entre Peso, Altura e IMC
st.header("Relação entre IMC, Peso e Altura")
fig_scatter_imc = px.scatter(
    df_selection,
    x="Weight",
    y="Height",
    size="BMI",
    color="Obesity",
    hover_name="Obesity",
    title="Relação Peso vs. Altura, dimensionado por IMC",
    labels={'Weight': 'Peso (kg)', 'Height': 'Altura (m)', 'Obesity': 'Nível de Obesidade'},
    size_max=60
)
st.plotly_chart(fig_scatter_imc, use_container_width=True)

# 4. Insights do Modelo Preditivo
if model:
    st.header("Principais Fatores Preditivos (Feature Importances)")
    st.markdown("""
    Este gráfico mostra quais características o modelo de Machine Learning considerou mais importantes
    para prever o nível de obesidade. Quanto maior a barra, mais "peso" o fator teve na decisão do modelo.
    """)

    try:
        # Extrair o pré-processador e o classificador do pipeline
        preprocessor = model.named_steps['preprocessor']
        classifier = model.named_steps['classifier']

        # Obter os nomes das features após o OneHotEncoding
        feature_names = preprocessor.get_feature_names_out()

        # Obter a importância das features
        importances = classifier.feature_importances_

        # Criar um DataFrame para visualização
        df_importances = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
        df_importances = df_importances.sort_values(by='Importance', ascending=False)

        # Gráfico de importância
        fig_importances = px.bar(
            df_importances,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Importância de Cada Fator para o Modelo',
            labels={'Feature': 'Fator', 'Importance': 'Importância'}
        )
        fig_importances.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_importances, use_container_width=True)
    except Exception as e:
        st.error(f"Não foi possível gerar o gráfico de importância das features: {e}")

else:
    st.warning(
        "O arquivo 'obesity_model.pkl' não foi encontrado, portanto não é possível exibir os insights do modelo.")
