import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Simulador SPA - AF Coimbra", page_icon="⚽", layout="wide")

# Dados Base Iniciais (Conforme as imagens fornecidas)
TABELA_INICIAL = {
    "ADC Almalaguês": {"P": 36, "J": 14, "GM": 38, "GS": 11},
    "COJA": {"P": 25, "J": 14, "GM": 34, "GS": 26},
    "União 1919 B": {"P": 20, "J": 13, "GM": 23, "GS": 18},
    "S. Pedro Alva": {"P": 19, "J": 14, "GM": 27, "GS": 24},
    "São Silvestre": {"P": 19, "J": 13, "GM": 16, "GS": 18},
    "CDR Vasco da Gama": {"P": 15, "J": 13, "GM": 14, "GS": 20},
    "Gândaras": {"P": 13, "J": 13, "GM": 13, "GS": 20},
    "Góis": {"P": 12, "J": 13, "GM": 23, "GS": 26},
    "UDR Cernache": {"P": 3, "J": 13, "GM": 12, "GS": 37}
}

# Lista de Jogos Ordenada por Jornada
jogos = [
    # Jornada 16
    {"j": 16, "c": "São Silvestre", "f": "S. Pedro Alva"},
    {"j": 16, "c": "Gândaras", "f": "União 1919 B"},
    {"j": 16, "c": "CDR Vasco da Gama", "f": "Góis"},
    {"j": 16, "c": "ADC Almalaguês", "f": "UDR Cernache"},
    # Jornada 17
    {"j": 17, "c": "Góis", "f": "São Silvestre"},
    {"j": 17, "c": "COJA", "f": "ADC Almalaguês"},
    {"j": 17, "c": "União 1919 B", "f": "CDR Vasco da Gama"},
    {"j": 17, "c": "UDR Cernache", "f": "Gândaras"},
    # Jornada 18
    {"j": 18, "c": "S. Pedro Alva", "f": "Góis"},
    {"j": 18, "c": "CDR Vasco da Gama", "f": "UDR Cernache"},
    {"j": 18, "c": "São Silvestre", "f": "União 1919 B"},
    {"j": 18, "c": "Gândaras", "f": "COJA"},
]

st.title("⚽ Simulador de Qualificação: São Pedro de Alva")
st.markdown("Preencha os resultados abaixo e clique em calcular para ver o impacto na tabela.")

# Estado para controlar se a tabela deve ser calculada
if 'calculado' not in st.session_state:
    st.session_state.calculado = False

# Função para resetar tudo
def limpar_resultados():
    for i in range(len(jogos)):
        st.session_state[f"c{i}"] = 0
        st.session_state[f"f{i}"] = 0
    st.session_state.calculado = False

# --- ÁREA DE INPUTS ---
st.header("📝 Resultados das Jornadas")
col_j16, col_j17, col_j18 = st.columns(3)

res_temp = []

# Jornada 16
with col_j16:
    st.info("Jornada 16 (Adiada)")
    for i, jogo in enumerate(jogos):
        if jogo['j'] == 16:
            c1, c2 = st.columns(2)
            gc = c1.number_input(f"{jogo['c']}", min_value=0, step=1, key=f"c{i}")
            gf = c2.number_input(f"{jogo['f']}", min_value=0, step=1, key=f"f{i}")
            res_temp.append((jogo['c'], jogo['f'], gc, gf))

# Jornada 17
with col_j17:
    st.info("Jornada 17")
    for i, jogo in enumerate(jogos):
        if jogo['j'] == 17:
            c1, c2 = st.columns(2)
            gc = c1.number_input(f"{jogo['c']}", min_value=0, step=1, key=f"c{i}")
            gf = c2.number_input(f"{jogo['f']}", min_value=0, step=1, key=f"f{i}")
            res_temp.append((jogo['c'], jogo['f'], gc, gf))

# Jornada 18
with col_j18:
    st.info("Jornada 18")
    for i, jogo in enumerate(jogos):
        if jogo['j'] == 18:
            c1, c2 = st.columns(2)
            gc = c1.number_input(f"{jogo['c']}", min_value=0, step=1, key=f"c{i}")
            gf = c2.number_input(f"{jogo['f']}", min_value=0, step=1, key=f"f{i}")
            res_temp.append((jogo['c'], jogo['f'], gc, gf))

# --- BOTÕES ---
st.write("---")
btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1:
    if st.button("🚀 Calcular Tabela", type="primary"):
        st.session_state.calculado = True
with btn_col2:
    if st.button("🗑️ Limpar Resultados", on_click=limpar_resultados):
        st.rerun()

# --- CÁLCULO E EXIBIÇÃO ---
if st.session_state.calculado:
    # Copia a tabela inicial para não corromper os dados
    t_final = {k: v.copy() for k, v in TABELA_INICIAL.items()}
    
    # Processa os resultados inseridos
    for casa, fora, gc, gf in res_temp:
        t_final[casa]["J"] += 1; t_final[fora]["J"] += 1
        t_final[casa]["GM"] += gc; t_final[casa]["GS"] += gf
        t_final[fora]["GM"] += gf; t_final[fora]["GS"] += gc
        if gc > gf: t_final[casa]["P"] += 3
        elif gf > gc: t_final[fora]["P"] += 3
        else: t_final[casa]["P"] += 1; t_final[fora]["P"] += 1

    # Criar DataFrame para visualização
    df = pd.DataFrame.from_dict(t_final, orient='index')
    df['DG'] = df['GM'] - df['GS']
    df = df.sort_values(by=['P', 'DG', 'GM'], ascending=False).reset_index()
    df = df.rename(columns={'index': 'Equipa'})
    df.index += 1 # Posição na tabela

    st.header("📊 Classificação Simulada")
    st.table(df[['Equipa', 'P', 'J', 'GM', 'GS', 'DG']])

    # Mensagem de Qualificação
    pos_spa = df[df['Equipa'] == "S. Pedro Alva"].index[0]
    if pos_spa <= 3:
        st.success(f"🔥 EXCELENTE! O São Pedro de Alva ficaria em {pos_spa}º lugar e qualifica-se!")
    else:
        st.error(f"⚠️ O SPA ficaria em {pos_spa}º lugar. Precisamos de outros resultados.")
else:
    st.info("Aguardando inserção de resultados para atualizar a classificação final.")
