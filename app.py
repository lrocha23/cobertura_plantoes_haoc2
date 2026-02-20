import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Plantões UTI", layout="wide")

# ============================
# 0) SENHA ÚNICA PARA TODOS
# ============================
SENHA = "1234"  # <<< TROQUE AQUI

senha_digitada = st.sidebar.text_input("Senha de acesso", type="password")

if senha_digitada != SENHA:
    st.warning("Digite a senha correta para acessar.")
    st.stop()

# ============================
# 1) Carrega lista oficial de médicos
# ============================
medicos_df = pd.read_csv("medicos.csv")
nomes_medicos = medicos_df["nome"].tolist()

# ============================
# 2) Carrega o CSV de plantões
# ============================
CSV_PATH = "/tmp/plantoes.csv"

if not os.path.exists(CSV_PATH):
    df_original = pd.read_csv("plantoes.csv")
    df_original.to_csv(CSV_PATH, index=False)

df = pd.read_csv(CSV_PATH)

# ============================
# 3) Configura dropdowns
# ============================
colunas_candidatos = ["candidato1", "candidato2", "candidato3", "candidato4", "candidato5"]

column_config = {
    col: st.column_config.SelectboxColumn(options=nomes_medicos)
    for col in colunas_candidatos
}

# ============================
# 4) Travar células já preenchidas
# ============================
disabled_cols = {}

for col in colunas_candidatos:
    disabled_cols[col] = df[col].notna() & (df[col] != "")

# ============================
# 5) Editor com dropdown
# ============================
st.title("📋 Inscrição de Plantões - UTI")

df_editado = st.data_editor(
    df,
    column_config=column_config,
    disabled=disabled_cols,
    key="editor",
    use_container_width=True
)

# ============================
# 6) Impedir duplicidade na mesma linha
# ============================
for idx, row in df_editado.iterrows():
    candidatos = [row[col] for col in colunas_candidatos]
    candidatos_limpos = [c for c in candidatos if c not in ["", None] and pd.notna(c)]

    if len(candidatos_limpos) != len(set(candidatos_limpos)):
        st.error(f"⚠️ Linha {idx+1}: o mesmo médico não pode aparecer duas vezes.")
        st.stop()

# ============================
# 7) Botão de salvar
# ============================
if st.button("Salvar alterações"):
    df_editado.to_csv(CSV_PATH, index=False)
    st.success("✔️ Salvo com sucesso! As escolhas agora estão travadas.")
    st.experimental_rerun()

# ============================
# 8) Exibe tabela final travada
# ============================
st.subheader("📌 Situação atual dos plantões")
st.dataframe(df_editado, use_container_width=True)