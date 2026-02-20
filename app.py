import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Plantões UTI", layout="wide")

# ============================
# 0) SENHA ÚNICA
# ============================
SENHA = "1234"

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
    col: st.column_config.SelectboxColumn(
        label=col,
        options=[""] + nomes_medicos,
        required=False
    )
    for col in colunas_candidatos
}

# ============================
# 4) Verifica se tabela já está travada
# ============================
travado = st.session_state.get("travado", False)

st.title("📋 Inscrição de Plantões - UTI")

if travado:
    st.success("✔️ A tabela está travada após o salvamento.")
    st.dataframe(df, use_container_width=True)
    st.stop()

# ============================
# 5) Editor com dropdown
# ============================
df_editado = st.data_editor(
    df,
    column_config=column_config,
    use_container_width=True,
    key="editor"
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
    st.session_state["travado"] = True
    st.success("✔️ Salvo com sucesso! A tabela agora está travada.")
    st.stop()

# ============================
# 8) Exibe tabela editável (antes de salvar)
# ============================
st.subheader("📌 Situação atual dos plantões")
st.dataframe(df_editado, use_container_width=True)
