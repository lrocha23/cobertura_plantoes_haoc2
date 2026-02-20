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

# Copia o CSV inicial para a pasta temporária se ainda não existir
if not os.path.exists(csv_temp):
    shutil.copy("plantoes.csv", csv_temp)

# Lê o CSV e garante que tudo é string
df = pd.read_csv(csv_temp, dtype=str).fillna("")

# Garante que as colunas de candidatos existem
for col in ["candidato1", "candidato2", "candidato3", "candidato4", "candidato5"]:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].astype(str).fillna("")

st.subheader("Candidaturas aos Plantões")

tabela_editada = st.data_editor(df)

if st.button("Salvar alterações"):
    # Recarrega o arquivo salvo antes de comparar
    df_original = pd.read_csv(csv_temp, dtype=str).fillna("")

    # Travamento de células preenchidas
    for linha in df.index:
        for coluna in ["candidato1", "candidato2", "candidato3", "candidato4", "candidato5"]:
            valor_antigo = df_original.loc[linha, coluna]
            valor_novo = tabela_editada.loc[linha, coluna]

            # Se já tinha nome, mantém o antigo
            if valor_antigo != "" and valor_novo != valor_antigo:
                tabela_editada.loc[linha, coluna] = valor_antigo

    # Salva o arquivo atualizado
    tabela_editada.to_csv(csv_temp, index=False)

    # Recarrega o arquivo salvo para refletir o travamento imediatamente
    df_atualizado = pd.read_csv(csv_temp, dtype=str).fillna("")
    st.dataframe(df_atualizado)

    st.success("Salvo com sucesso! Células preenchidas foram protegidas.")
