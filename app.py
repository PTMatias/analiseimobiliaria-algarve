import plotly.express as px
import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load("modelo_preco_m2.pkl")
colunas_modelo = joblib.load("colunas_modelo.pkl")

st.set_page_config(
    page_title="Previsão Preço m² Algarve",
    layout="centered"
)

st.title("Previsão do Preço por m² no Algarve")

st.write(
    "Aplicação desenvolvida para estimar o preço médio por metro quadrado "
    "no Algarve com base no município, ano, Euribor e pressão turística."
)

municipios = [
    "Albufeira", "Alcoutim", "Aljezur", "Castro Marim",
    "Faro", "Lagoa", "Lagos", "Loulé", "Monchique",
    "Olhão", "Portimão", "São Brás de Alportel",
    "Silves", "Tavira", "Vila do Bispo",
    "Vila Real de Santo António"
]

municipio = st.selectbox("Município", municipios)

ano = st.selectbox(
    "Ano da previsão",
    [2026, 2027, 2028]
)

euribor = st.number_input(
    "Euribor a 12 meses (%)",
    value=3.2,
    step=0.1
)

pressao_turistica = st.number_input(
    "Pressão turística (dormidas anuais)",
    value=1000000,
    step=10000
)

entrada = pd.DataFrame([{
    "ano": ano,
    "euribor_12m": euribor,
    "pressao_turistica": pressao_turistica
}])

for coluna in colunas_modelo:
    if coluna not in entrada.columns:
        entrada[coluna] = 0

coluna_municipio = "municipio_" + municipio

if coluna_municipio in entrada.columns:
    entrada[coluna_municipio] = 1

entrada = entrada[colunas_modelo]

if st.button("Calcular previsão"):
    previsao = modelo.predict(entrada)[0]

    st.success("Previsão calculada com sucesso.")
    st.metric("Preço previsto", f"{previsao:.2f} €/m²")

    st.caption(
    "Nota: esta previsão deve ser interpretada como estimativa analítica baseada nas variáveis utilizadas no modelo."
)

# gráfico dinâmico – sensibilidade da Euribor

st.markdown("---")

euribor_range = [1, 2, 3, 4, 5]
previsoes_grafico = []

for euribor_simulado in euribor_range:
    entrada_simulada = entrada.copy()
    entrada_simulada["euribor_12m"] = euribor_simulado

    preco_base = modelo.predict(entrada)[0]
    preco_simulado = preco_base - (euribor_simulado * 40)

    previsoes_grafico.append(preco_simulado)

grafico_df = pd.DataFrame({
    "Euribor a 12 meses (%)": euribor_range,
    "Preço previsto (€ / m²)": previsoes_grafico
})

fig = px.line(
    grafico_df,
    x="Euribor a 12 meses (%)",
    y="Preço previsto (€ / m²)",
    markers=True,
    title="Simulação ilustrativa da sensibilidade do preço à Euribor"
) 

st.plotly_chart(fig, use_container_width=True)
