import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador SPA - AF Coimbra", page_icon="⚽")

st.title("⚽ Simulador de Qualificação: São Pedro de Alva")
st.markdown("Preencha os resultados das próximas jornadas para ver a classificação final.")

# Dados Base
if 'tabela' not in st.session_state:
    st.session_state.tabela = {
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

jogos = [
    {"j": 17, "c": "Góis", "f": "São Silvestre"},
    {"j": 17, "c": "COJA", "f": "ADC Almalaguês"},
    {"j": 17, "c": "União 1919 B", "f": "CDR Vasco da Gama"},
    {"j": 17, "c": "UDR Cernache", "f": "Gândaras"},
    {"j": 18, "c": "S. Pedro Alva", "f": "Góis"},
    {"j": 18, "c": "CDR Vasco da Gama", "f": "UDR Cernache"},
    {"j": 18, "c": "São Silvestre", "f": "União 1919 B"},
    {"j": 18, "c": "Gândaras", "f": "COJA"},
    {"j": 16, "c": "São Silvestre", "f": "S. Pedro Alva"},
    {"j": 16, "c": "Gândaras", "f": "União 1919 B"},
    {"j": 16, "c": "CDR Vasco da Gama", "f": "Góis"},
]

# Interface para preencher resultados
resultados = []
with st.sidebar:
    st.header("Preencher Resultados")
    for i, jogo in enumerate(jogos):
        st.subheader(f"Jornada {jogo['j']}")
        col1, col2 = st.columns(2)
        with col1: gc = st.number_input(f"{jogo['c']}", min_value=0, step=1, key=f"c{i}")
        with col2: gf = st.number_input(f"{jogo['f']}", min_value=0, step=1, key=f"f{i}")
        resultados.append((jogo['c'], jogo['f'], gc, gf))

# Cálculo da Classificação
t_final = {k: v.copy() for k, v in st.session_state.tabela.items()}
for c, f, gc, gf in resultados:
    t_final[c]["J"] += 1; t_final[f]["J"] += 1
    t_final[c]["GM"] += gc; t_final[c]["GS"] += gf
    t_final[f]["GM"] += gf; t_final[f]["GS"] += gc
    if gc > gf: t_final[c]["P"] += 3
    elif gf > gc: t_final[f]["P"] += 3
    else: t_final[c]["P"] += 1; t_final[f]["P"] += 1

df = pd.DataFrame.from_dict(t_final, orient='index')
df['DG'] = df['GM'] - df['GS']
df = df.sort_values(by=['P', 'DG', 'GM'], ascending=False).reset_index()
df.index += 1

st.table(df[['index', 'P', 'J', 'GM', 'GS', 'DG']].rename(columns={'index': 'Equipa'}))

# Alerta de Qualificação
pos_spa = df[df['Equipa'] == "S. Pedro Alva"].index[0]
if pos_spa <= 3:
    st.success(f"✅ O São Pedro de Alva qualifica-se em {pos_spa}º lugar!")
else:
    st.error(f"❌ O SPA ficaria em {pos_spa}º lugar.")
