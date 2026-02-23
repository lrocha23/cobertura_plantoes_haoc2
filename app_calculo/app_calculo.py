import streamlit as st
import pandas as pd
import random

st.title("Cálculo Inclusivo da Escala – App Privado (versão sem IDs)")

# ============================
# 1) Upload dos arquivos
# ============================
st.header("Envio dos arquivos")

arquivo_inscricoes = st.file_uploader(
    "Envie o arquivo de inscrições (ex: plantoes_final_mar26.csv)",
    type=["csv"]
)

arquivo_ano = st.file_uploader(
    "Envie o histórico anual (historico_ano.csv)",
    type=["csv"]
)

arquivo_mes = st.file_uploader(
    "Envie o histórico do último mês (historico_ultimo_mes.csv)",
    type=["csv"]
)

if not (arquivo_inscricoes and arquivo_ano and arquivo_mes):
    st.stop()

df = pd.read_csv(arquivo_inscricoes)
historico_ano = pd.read_csv(arquivo_ano)
historico_mes = pd.read_csv(arquivo_mes)

# ============================
# 2) Preparação dos dados
# ============================
st.header("Processamento dos dados")

colunas_candidatos = ["candidato1","candidato2","candidato3","candidato4","candidato5"]

def get_candidatos(row):
    return [
        nome
        for nome in [row[c] for c in colunas_candidatos]
        if isinstance(nome, str) and nome.strip() != ""
    ]

# Dicionários: nome → plantoes
plant_ano = dict(zip(historico_ano.nome, historico_ano.plantoes))
plant_mes = dict(zip(historico_mes.nome, historico_mes.plantoes))

# ============================
# 3) Função de escore
# ============================
def calcular_escore(nome_medico, ganhos_rodada):
    return (
        plant_ano.get(nome_medico, 0) * 1.5 +
        plant_mes.get(nome_medico, 0) * 3 +
        ganhos_rodada.get(nome_medico, 0) * 2 +
        random.random()
    )

# ============================
# 4) Calcular recomendados
# ============================
st.header("Recomendações do algoritmo")

ganhos_rodada = {}
recomendados = {}

for idx, row in df.iterrows():
    candidatos = get_candidatos(row)

    if len(candidatos) == 0:
        recomendados[idx] = None
        continue

    if len(candidatos) == 1:
        escolhido = candidatos[0]
        recomendados[idx] = escolhido
        ganhos_rodada[escolhido] = ganhos_rodada.get(escolhido, 0) + 1
        continue

    scores = {nome: calcular_escore(nome, ganhos_rodada) for nome in candidatos}

    escolhido = min(scores, key=scores.get)
    recomendados[idx] = escolhido

    ganhos_rodada[escolhido] = ganhos_rodada.get(escolhido, 0) + 1

# ============================
# 5) Interface de escolha manual
# ============================
st.header("Escolha manual com sugestão")

escolhas_finais = []

for idx, row in df.iterrows():
    candidatos = get_candidatos(row)
    recomendado = recomendados[idx]

    st.subheader(f"{row['data']} - {row['horario']} (vagas: {row['vagas']})")

    if not candidatos:
        st.info("Nenhum candidato inscrito.")
        escolhas_finais.append((idx, None))
        continue

    st.write(f"Recomendado pelo algoritmo: **{recomendado}**")

    index_recomendado = candidatos.index(recomendado)

    escolha_nome = st.radio(
        "Escolha final:",
        candidatos,
        index=index_recomendado,
        key=f"escolha_{idx}"
    )

    escolhas_finais.append((idx, escolha_nome))

# ============================
# 6) Gerar escala final
# ============================
st.header("Gerar escala final")

if st.button("Baixar escala final"):
    for idx, nome_escolhido in escolhas_finais:
        df.loc[idx, "plantonista"] = nome_escolhido

    csv_final = df.to_csv(index=False)

    st.download_button(
        "Clique para baixar a escala final",
        csv_final,
        file_name="escala_final.csv",
        mime="text/csv"
    )

    st.success("Escala final gerada com sucesso!")
