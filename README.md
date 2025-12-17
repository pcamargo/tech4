# Tech Challenge - Fase 04

Desenvolvimento de uma aplicação de modelo preditivo para
auxiliar a tomada de decisão da equipe médica a diagnosticar a obesidade

# Página Streamlit
https://rm362113-tech4.streamlit.app/

## Repositório
git remote add origin https://github.com/pcamargo/tech4.git
git branch -M main
git push -u origin main

## Desenvolvimento com PyCharm
Para desenvolver e executar o projeto no PyCharm, seguir os passos abaixo:

1.  **Clonar o Repositório:**
    *   Use o Git para clonar o repositório para a máquina local.

2.  **Abrir o Projeto no PyCharm:**
    *   Abrir o PyCharm e selecionar "Open" (ou "File" > "Open").
    *   Navegar até a pasta do projeto e selecionar.

3.  **Instalar as Dependências:**
    *   Abrir o terminal do PyCharm (`View` > `Tool Windows` > `Terminal`) e executar:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Executando os Scripts:**
    *   **Para treinar o modelo:** Executar o script `src/main.py`. Isso irá gerar o arquivo `obesity_model.pkl`.
    *   **Para iniciar o servidor web local:** Executar o script `src/server.py`.
    *   **Para rodar a aplicação Streamlit local:** Abrir o terminal do PyCharm e executar `streamlit run home.py`.

## Testar localmente
Testar a aplicação localmente antes de fazer o deploy, para garantir que tudo funciona como esperado.

### Testar com http request
* Subir a aplicação web executando o script python server.py
* Executar o script http sample_post.http

### Testar com Streamlit
* Abrir o terminal na pasta onde os arquivos estão localizados.
* Executar a aplicação com o comando: streamlit run app.py
* O Streamlit abrirá uma o navegador com a interface da aplicação.

## Deploy com Streamlit Community Cloud
Obter uma conta gratuita no Stramlit e seguir os passos abaixo.
O Streamlit vai construir a aplicação, instalar as dependências a publicar
* Criar um novo repositório públic no GitHub
* Colocar os três arquivos (app.py, obesity_model.pkl, requirements.txt) no repositório do GitHub
* Acessar o site https://streamlit.io/cloud e fazer login com a conta do GitHub
* No painel do Streamlit Cloud, clique em "Create app"
* Selecionar o repositório, o branch e o arquivo principal (app.py)
* Clicar em "Deploy!".

## Dicioinário de Dados

### Demographics and physical attributes
- **Gender**: The sex of the individual.
- **Age**: The person's age in years.
- **Height**: The person's height in meters.
- **Weight**: The person's weight in kilograms.
- **family_history_with_overweight**: Indicates whether a person has a family history of being overweight (yes/no). 

### Eating habits
- **FAVC (Frequent consumption of high caloric food)**: Indicates if the person frequently consumes high-calorie foods (yes/no).
- **FCVC (Frequency of consumption of vegetables)**: Frequency of vegetable consumption on a scale from 1 to 3.
- **NCP (Number of main meals)**: The number of main meals a person has per day.
- **CAEC (Consumption of food between meals)**: Frequency of eating food between main meals (e.g., Never, Sometimes, Frequently, Always).
- **CH2O (Consumption of water daily)**: Indicates the daily water intake on a scale from 1 to 3.
- **CALC (Consumption of alcohol)**: Frequency of alcohol consumption (e.g., Never, Sometimes, Frequently, Always). 

### LifestylePhysical activity and technology use
- **SCC (Calories consumption monitoring)**: Indicates if the person monitors their daily calorie intake (yes/no).
- **FAF (Physical activity frequency)**: Physical activity frequency per week on a scale from 0 to 3.
- **TUE (Time using technology devices)**: Time spent using technological devices daily, such as smartphones or computers, on a scale from 0 to 3.
- **MTRANS (Main mode of transportation)**: The person's main mode of transportation (e.g., Automobile, Bike, Motorbike, Public Transportation, Walking).
- 