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

# Tabela editável
tabela_editavel = st.data_editor(df, key="editor")

if st.button("Salvar alterações"):
    df_original = pd.read_csv(csv_temp, dtype=str).fillna("")

    # Travamento de células preenchidas
    for linha in df.index:
        for coluna in ["candidato1", "candidato2", "candidato3", "candidato4", "candidato5"]:
            valor_antigo = df_original.loc[linha, coluna]
            valor_novo = tabela_editavel.loc[linha, coluna]

            if valor_antigo != "" and valor_novo != valor_antigo:
                tabela_editavel.loc[linha, coluna] = valor_antigo

    tabela_editavel.to_csv(csv_temp, index=False)

    st.success("Salvo com sucesso! Células preenchidas foram protegidas.")

    # Recarrega o arquivo salvo e mostra SOMENTE a tabela travada
    df_travado = pd.read_csv(csv_temp, dtype=str).fillna("")
    st.subheader("Tabela atualizada (travada)")
    st.dataframe(df_travado)

    st.stop()
