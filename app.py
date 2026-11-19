import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Censo Demográfico de 1872", layout="wide")

df = pd.read_csv("censo_1872.csv")
df = df.drop_duplicates()

total_homens_livres = df["homens_livres"].sum()
total_homens_escravizados = df["homens_escravizados"].sum()
total_mulheres_livres = df["mulheres_livres"].sum()
total_mulheres_escravizadas = df["mulheres_escravizadas"].sum()

total_homens = total_homens_livres + total_homens_escravizados
perc_homens_livres = (total_homens_livres / total_homens) * 100
perc_homens_escravizados = (total_homens_escravizados / total_homens) * 100

total_mulheres = total_mulheres_livres + total_mulheres_escravizadas
perc_mulheres_livres = (total_mulheres_livres / total_mulheres) * 100
perc_mulheres_escravizadas = (total_mulheres_escravizadas / total_mulheres) * 100

st.title("Censo Demográfico do Brasil de 1872")

st.sidebar.title("Navegação")
opcao = st.sidebar.radio(
    "Selecione a visualização:",
    options=["Tabela", "Gráficos"]
)

if opcao == "Tabela":
    st.header("Tabela de Totais e Percentuais por Grupo")
    
    tabela_resumo = pd.DataFrame({
        "Grupo": [
            "Homens Livres",
            "Homens Escravizados",
            "Mulheres Livres",
            "Mulheres Escravizadas"
        ],
        "Total de Pessoas": [
            total_homens_livres,
            total_homens_escravizados,
            total_mulheres_livres,
            total_mulheres_escravizadas
        ],
        "Percentual no Grupo (%)": [
            round(perc_homens_livres, 2),
            round(perc_homens_escravizados, 2),
            round(perc_mulheres_livres, 2),
            round(perc_mulheres_escravizadas, 2)
        ]
    })
    
    st.dataframe(tabela_resumo, use_container_width=True, hide_index=True)

elif opcao == "Gráficos":
    st.header("Distribuição Percentual por Sexo e Divisão entre Livre e Escravizado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_homens = pd.DataFrame({
            "Condição": ["Homens Livres", "Homens Escravizados"],
            "Percentual": [perc_homens_livres, perc_homens_escravizados],
            "Total": [total_homens_livres, total_homens_escravizados]
        })
        fig_homens = px.pie(
            df_homens,
            names="Condição",
            values="Percentual",
            title="Homens: Livres vs Escravizados (%)",
            hover_data=["Total"]
        )
        fig_homens.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_homens, use_container_width=True)
        
    with col2:
        df_mulheres = pd.DataFrame({
            "Condição": ["Mulheres Livres", "Mulheres Escravizadas"],
            "Percentual": [perc_mulheres_livres, perc_mulheres_escravizadas],
            "Total": [total_mulheres_livres, total_mulheres_escravizadas]
        })
        fig_mulheres = px.pie(
            df_mulheres,
            names="Condição",
            values="Percentual",
            title="Mulheres: Livres vs Escravizadas (%)",
            hover_data=["Total"]
        )
        fig_mulheres.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_mulheres, use_container_width=True)

        st.markdown("base de dados aqui >>>> https://basedosdados.org/")


