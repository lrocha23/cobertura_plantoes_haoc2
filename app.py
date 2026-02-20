import streamlit as st
import pandas as pd
import os
import shutil

SENHA = "Vou_ajudar@26"

st.title("Escala de Plantão Médico – Março 2026")

senha_digitada = st.text_input("Digite a senha:", type="password")

if senha_digitada != SENHA:
    st.stop()

csv_temp = "/tmp/plantoes.csv"

if not os.path.exists(csv_temp):
    shutil.copy("plantoes.csv", csv_temp)

df = pd.read_csv(csv_temp, dtype=str)

# Garante que as colunas existem e são texto
for col in ["candidato1", "candidato2", "candidato3", "candidato4", "candidato5"]:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].astype(str)

st.subheader("Candidaturas aos Plantões")

tabela_editada = st.data_editor(df)

if st.button("Salvar alterações"):
    df_original = pd.read_csv(csv_temp, dtype=str)

    for linha in df.index:
        for coluna in ["candidato1", "candidato2", "candidato3", "candidato4", "candidato5"]:
            valor_antigo = df_original.loc[linha, coluna]
            valor_novo = tabela_editada.loc[linha, coluna]

            if valor_antigo != "" and valor_novo != valor_antigo:
                tabela_editada.loc[linha, coluna] = valor_antigo

    tabela_editada.to_csv(csv_temp, index=False)
    st.success("Salvo com sucesso! Células preenchidas foram protegidas.")
