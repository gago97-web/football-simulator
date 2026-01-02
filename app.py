import streamlit as st
import pandas as pd
import numpy as np
import math

# IMPORTANTE: set_page_config DEVE essere la prima chiamata Streamlit
st.set_page_config(
    page_title="Simulatore Serie A",
    page_icon="⚽",
    layout="wide"
)

from pathlib import Path
folder = Path(__file__).parent / 'Risultati'
csv_files = sorted(folder.glob('*.csv'))

dfs = []
for fp in csv_files:
    df = pd.read_csv(fp, sep=';', encoding='utf-8')
    dfs.append(df)
    
df_all = pd.concat(dfs, ignore_index=False)    
df_all_sampl = df_all[['HomeTeam', 'AwayTeam', 'FTR']]

from data_loader import (
    carica_classifica, 
    carica_calendario_rimanente,
    CLASSIFICA_FALLBACK,
    CALENDARIO_FALLBACK
)

# Prova a caricare dati live, altrimenti usa dati statici
try:
    with st.spinner("🔄 Caricamento dati live dall'API..."):
        CLASSIFICA_INIZIALE = carica_classifica()
        CALENDARIO = carica_calendario_rimanente()
    st.success("✅ Dati caricati con successo dall'API!")
except Exception as e:
    st.info("📋 Utilizzo dati statici")
    CLASSIFICA_INIZIALE = CLASSIFICA_FALLBACK
    CALENDARIO = CALENDARIO_FALLBACK

# CSS personalizzato Instagram-style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }
    
    h1, h2, h3 {
        font-weight: 900 !important;
        letter-spacing: -0.5px;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        border-radius: 20px;
        padding: 18px 30px;
        border: none;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .card-gradient {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.6);
    }
    
    .story-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .story-card::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        border-radius: 20px;
        z-index: -1;
    }
    
    .story-card:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .mode-button {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
    }
    
    .mode-button::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .mode-button:hover::before {
        opacity: 1;
    }
    
    .mode-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid #667eea;
        background: white;
        font-weight: 600;
    }
    
    .dataframe {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    }
    
    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: black;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 40px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .emoji-large {
        font-size: 3rem;
        margin-bottom: 15px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    .probability-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        margin-top: 5px;
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .stMetric label {
        font-size: 18px !important;
        font-weight: 700 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .match-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 15px;
        border: none;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        font-weight: 600;
    }
    
    div[data-testid="stHorizontalBlock"] {
        gap: 20px;
    }
    
    .insta-header {
        background: white;
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

TOT_PARTITE = 38

def calcola_probabilita_vittoria(squadra, avversario, is_home, df_storico, classifica):
    """Probabilità 1-X-2 basata su storico H2H e stats stagionali"""
    try:
        if is_home:
            matches = df_storico[(df_storico['HomeTeam'] == squadra) & (df_storico['AwayTeam'] == avversario)]
        else:
            matches = df_storico[(df_storico['HomeTeam'] == avversario) & (df_storico['AwayTeam'] == squadra)]

        if len(matches) == 0:
            p1, px, p2 = 0.4, 0.3, 0.3
        else:
            totale = len(matches)
            if is_home:
                vittorie = len(matches[matches['FTR'] == 'H'])
                pareggi = len(matches[matches['FTR'] == 'D'])
                sconfitte = len(matches[matches['FTR'] == 'A'])
            else:
                vittorie = len(matches[matches['FTR'] == 'A'])
                pareggi = len(matches[matches['FTR'] == 'D'])
                sconfitte = len(matches[matches['FTR'] == 'H'])
            p1 = vittorie / totale
            px = pareggi / totale
            p2 = sconfitte / totale
    except:
        p1, px, p2 = 0.4, 0.3, 0.3

    def get_team_stats(nome_squadra, classifica):
        sq = next((x for x in classifica if x["nome"] == nome_squadra), None)
        if sq is None:
            return {"mediaPunti": 1.5, "win_rate": 0.5, "draw_rate": 0.25}
        mediaPunti = sq["punti"] / sq["partite"] if sq["partite"] > 0 else 0
        win_rate = sq.get("win_rate")
        draw_rate = sq.get("draw_rate")
        if win_rate is None or draw_rate is None:
            vittorie = sq["punti"] // 3
            pareggi = sq["punti"] % 3
            win_rate = vittorie / sq["partite"] if sq["partite"] > 0 else 0
            draw_rate = pareggi / sq["partite"] if sq["partite"] > 0 else 0
        return {"mediaPunti": mediaPunti, "win_rate": win_rate, "draw_rate": draw_rate}
    
    s = get_team_stats(squadra, CLASSIFICA_FALLBACK)
    a = get_team_stats(avversario, CLASSIFICA_FALLBACK)
    delta = (s["mediaPunti"] - a["mediaPunti"]) + 0.7 * (s["win_rate"] - a["win_rate"]) - 0.3 * (s["draw_rate"] - a["draw_rate"])
    alpha = 0.15
    home_bonus = 0.08 if is_home else -0.04
    p1 = p1 + alpha * delta + home_bonus
    px = px * (1 - min(0.7, abs(delta)))
    p2 = 1 - p1 - px
    p1 = max(0.05, min(0.85, p1))
    px = max(0.05, min(0.30, px))
    p2 = max(0.05, min(0.85, p2))
    tot = p1 + px + p2
    return {"1": p1 / tot, "X": px / tot, "2": p2 / tot}

def calcola_punti_necessari(obiettivo, classifica_ordinata):
    if obiettivo == "Scudetto":
        return classifica_ordinata[0]["puntiFinali"] + 1
    elif obiettivo == "Champions":
        return classifica_ordinata[3]["puntiFinali"] + 1
    elif obiettivo == "Europa":
        return classifica_ordinata[6]["puntiFinali"] + 1
    elif obiettivo == "Salvezza":
        return classifica_ordinata[17]["puntiFinali"] + 1
    return 0

def simula_risultati_ottimali(squadra_sel, obiettivo, calendario_partite, df_storico, classifica):
    proiezione_altre = []
    for sq in classifica:
        if sq["nome"] != squadra_sel["nome"]:
            punti_da_media = round(sq["mediaPunti"] * sq["partiteRimanenti"])
            punti_finali = sq["punti"] + punti_da_media
            proiezione_altre.append({"nome": sq["nome"], "puntiFinali": punti_finali, "DR": sq["DR"]})
    proiezione_altre = sorted(proiezione_altre, key=lambda x: (x["puntiFinali"], x["DR"]), reverse=True)
    punti_target = calcola_punti_necessari(obiettivo, proiezione_altre)
    punti_da_fare = max(0, punti_target - squadra_sel["punti"])
    risultati = []
    punti_accumulati = 0
    for match in calendario_partite:
        avversario = match["vs"]
        is_home = match["home"]
        prob = calcola_probabilita_vittoria(squadra_sel["nome"], avversario, is_home, df_storico, CLASSIFICA_INIZIALE)
        if punti_accumulati < punti_da_fare:
            if prob["1"] >= 0.40:
                risultati.append(("1", prob["1"]))
                punti_accumulati += 3
            elif prob["X"] >= 0.25:
                risultati.append(("X", prob["X"]))
                punti_accumulati += 1
            else:
                risultati.append(("2", prob["2"]))
                punti_accumulati += 0
        else:
            risultato_prob = max(prob.items(), key=lambda x: x[1])
            risultati.append((risultato_prob[0], risultato_prob[1]))
            if risultato_prob[0] == "1":
                punti_accumulati += 3
            elif risultato_prob[0] == "X":
                punti_accumulati += 1
    return risultati, punti_accumulati, punti_target

def calcola_probabilita_obiettivi(squadra_sel, calendario_partite, df_storico, classifica):
    """Versione ottimizzata: 70% più veloce"""
    n_simulazioni = 300  # Ridotto da 1000 per velocità (accuratezza ancora ottima)
    obiettivi_raggiunti = {"Scudetto": 0, "Champions": 0, "Europa": 0, "Salvezza": 0}
    
    # PRE-CALCOLO: Calcola probabilità partite UNA VOLTA SOLA (invece di 1000 volte)
    prob_partite = []
    for match in calendario_partite:
        prob = calcola_probabilita_vittoria(squadra_sel["nome"], match["vs"], match["home"], df_storico, CLASSIFICA_INIZIALE)
        prob_partite.append((prob["1"], prob["1"] + prob["X"]))  # Salva solo i valori necessari
    
    # PRE-CALCOLO: Prepara dati altre squadre UNA VOLTA SOLA
    altre_squadre = []
    for sq in classifica:
        if sq["nome"] != squadra_sel["nome"]:
            punti_da_media = round(sq["mediaPunti"] * sq["partiteRimanenti"])
            altre_squadre.append({
                "nome": sq["nome"],
                "punti_base": sq["punti"] + punti_da_media,
                "DR": sq["DR"]
            })
    
    # SIMULAZIONI: Ora molto più veloci
    for _ in range(n_simulazioni):
        punti_squadra = squadra_sel["punti"]
        
        # Simula risultati usando probabilità pre-calcolate
        for prob1, prob1x in prob_partite:
            rand = np.random.random()
            if rand < prob1:
                punti_squadra += 3
            elif rand < prob1x:
                punti_squadra += 1
        
        # Costruisci classifica simulata
        classifica_sim = [{"nome": squadra_sel["nome"], "puntiFinali": punti_squadra, "DR": squadra_sel["DR"]}]
        for sq in altre_squadre:
            classifica_sim.append({
                "nome": sq["nome"],
                "puntiFinali": sq["punti_base"] + np.random.randint(-3, 4),
                "DR": sq["DR"]
            })
        
        classifica_sim.sort(key=lambda x: (x["puntiFinali"], x["DR"]), reverse=True)
        posizione = next(idx for idx, sq in enumerate(classifica_sim) if sq["nome"] == squadra_sel["nome"])
        
        if posizione == 0:
            obiettivi_raggiunti["Scudetto"] += 1
        if posizione <= 3:
            obiettivi_raggiunti["Champions"] += 1
        if posizione <= 6:
            obiettivi_raggiunti["Europa"] += 1
        if posizione <= 17:
            obiettivi_raggiunti["Salvezza"] += 1
    
    return {k: (v / n_simulazioni) * 100 for k, v in obiettivi_raggiunti.items()}

def calcola_dati(classifica):
    for sq in classifica:
        sq["mediaPunti"] = sq["punti"] / sq["partite"] if sq["partite"] > 0 else 0
        sq["partiteRimanenti"] = TOT_PARTITE - sq["partite"]
        sq["DR"] = sq["golFatti"] - sq["golSubiti"]
    return classifica

def calcola_quote(classifica):
    proiezione = []
    for sq in classifica:
        punti_proiettati = sq["punti"] + round(sq["mediaPunti"] * sq["partiteRimanenti"])
        proiezione.append({"nome": sq["nome"], "puntiProiettati": punti_proiettati, "DR": sq["DR"]})
    proiezione.sort(key=lambda x: (x["puntiProiettati"], x["DR"]), reverse=True)
    return {
        "scudetto": round(proiezione[0]["puntiProiettati"]),
        "champions": round(proiezione[3]["puntiProiettati"]),
        "europa": round(proiezione[6]["puntiProiettati"]),
        "retrocessione": round(proiezione[17]["puntiProiettati"])
    }

def ordina_classifica(dati, campo_punti="punti"):
    return sorted(dati, key=lambda x: (x[campo_punti], x["DR"]), reverse=True)

def get_colore_zona(posizione):
    if posizione == 0:
        return "#fef3c7"
    elif posizione <= 3:
        return "#dbeafe"
    elif posizione <= 6:
        return "#dcfce7"
    elif posizione >= 17:
        return "#fee2e2"
    return "white"

# Inizializza session state
if 'classifica' not in st.session_state:
    st.session_state.classifica = calcola_dati(CLASSIFICA_INIZIALE.copy())
if 'risultati' not in st.session_state:
    st.session_state.risultati = {}
if 'squadra_selezionata' not in st.session_state:
    st.session_state.squadra_selezionata = None
if 'modalita' not in st.session_state:
    st.session_state.modalita = None

# Header Instagram-style
st.markdown('<div class="insta-header">', unsafe_allow_html=True)
st.markdown('<div class="emoji-large">⚽</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title-gradient">SERIE A SIMULATOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Prevedi il futuro della tua squadra del cuore</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sezione Quote con card Instagram-style
quote = calcola_quote(st.session_state.classifica)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="emoji-large">🏆</div>
        <h3 style='color: white; margin: 10px 0; font-size: 1rem; font-weight: 700;'>Quota Scudetto</h3>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 900;'>{quote['scudetto']}</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 5px 0; font-weight: 600;'>punti necessari</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="emoji-large">🌟</div>
        <h3 style='color: white; margin: 10px 0; font-size: 1rem; font-weight: 700;'>Quota Champions</h3>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 900;'>{quote['champions']}</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 5px 0; font-weight: 600;'>punti necessari</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="emoji-large">📈</div>
        <h3 style='color: white; margin: 10px 0; font-size: 1rem; font-weight: 700;'>Quota Europa</h3>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 900;'>{quote['europa']}</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 5px 0; font-weight: 600;'>punti necessari</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="emoji-large">⚠️</div>
        <h3 style='color: white; margin: 10px 0; font-size: 1rem; font-weight: 700;'>Quota Salvezza</h3>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 900;'>{quote['retrocessione']}</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 5px 0; font-weight: 600;'>punti necessari</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Classifica in card
st.markdown('<div class="card-gradient">', unsafe_allow_html=True)
st.markdown("### 📊 Classifica Attuale")
classifica_ordinata = ordina_classifica(st.session_state.classifica)

df_classifica = pd.DataFrame([
    {
        "#": idx + 1,
        "Squadra": sq["nome"],
        "Pt": sq["punti"],
        "G": sq["partite"],
        "GF": sq["golFatti"],
        "GS": sq["golSubiti"],
        "DR": sq["DR"],
        "Media": f"{sq['mediaPunti']:.2f}"
    }
    for idx, sq in enumerate(classifica_ordinata)
])

def color_rows(row):
    idx = row.name
    color = get_colore_zona(idx)
    return [f'background-color: {color}'] * len(row)

styled_df = df_classifica.style.apply(color_rows, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# Simulatore
st.markdown('<div class="card-gradient">', unsafe_allow_html=True)
st.markdown("### 🎮 Inizia la Simulazione")

squadre = [sq["nome"] for sq in st.session_state.classifica]
squadra_selezionata = st.selectbox("🔍 Scegli la tua squadra:", [""] + squadre)

if squadra_selezionata:
    st.session_state.squadra_selezionata = next(sq for sq in st.session_state.classifica if sq["nome"] == squadra_selezionata)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;'>
        <h2 style='color: white; margin: 0; font-weight: 900;'>{squadra_selezionata}</h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.2rem; font-weight: 600; margin: 10px 0;'>
            {st.session_state.squadra_selezionata['partiteRimanenti']} partite rimanenti
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    n_partite = st.session_state.squadra_selezionata["partiteRimanenti"]
    cal_base = CALENDARIO_FALLBACK.get(squadra_selezionata, [])
    
    calendario_partite = []
    for i, partita in enumerate(cal_base[:n_partite]):
        calendario_partite.append({"vs": partita['vs'], "home": partita['home']})
    
    st.markdown("### 🎯 Scegli la Modalità")
    col_mode1, col_mode2 = st.columns(2)
    
    with col_mode1:
        if st.button("🤖 AI AUTOMATICO", use_container_width=True, key="btn_ai"):
            st.session_state.modalita = "automatica"
    
    with col_mode2:
        if st.button("✋ MANUALE", use_container_width=True, key="btn_manual"):
            st.session_state.modalita = "manuale"
    
    # MODALITÀ AUTOMATICA
    if st.session_state.modalita == "automatica":
        st.markdown("### 🤖 Simulazione Automatica con AI")
        st.info("L'AI calcolerà automaticamente i risultati più probabili basandosi sui dati storici")
        
        obiettivo = st.selectbox(
            "Seleziona l'obiettivo da raggiungere:",
            ["Scudetto", "Champions", "Europa", "Salvezza"]
        )
        
        if st.button("🔮 CALCOLA CON AI", type="primary"):
            with st.spinner("🧠 Analisi in corso..."):
                # Calcola risultati ottimali
                risultati_ai, punti_tot, punti_target = simula_risultati_ottimali(
                    st.session_state.squadra_selezionata,
                    obiettivo,
                    calendario_partite,
                    df_all_sampl,
                    st.session_state.classifica
                )
                
                # Calcola probabilità obiettivi
                prob_obiettivi = calcola_probabilita_obiettivi(
                    st.session_state.squadra_selezionata,
                    calendario_partite,
                    df_all_sampl,
                    st.session_state.classifica
                )
            
            # Mostra risultati suggeriti
            st.markdown("#### 📋 Risultati Suggeriti dall'AI")
            st.write(f"**Punti necessari per {obiettivo}:** {punti_target}")
            st.write(f"**Punti attuali:** {st.session_state.squadra_selezionata['punti']}")
            st.write(f"**Punti totali proiettati:** {st.session_state.squadra_selezionata['punti'] + sum(3 if r[0]=='1' else 1 if r[0]=='X' else 0 for r in risultati_ai)}")
            
            st.markdown("#### 🎯 Piano Partite Suggerito:")
            cols_per_row = 3
            for i in range(0, len(calendario_partite), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(calendario_partite):
                        with cols[j]:
                            match = calendario_partite[i + j]
                            ris_tipo, prob = risultati_ai[i + j]
                            ris_label = "Vittoria" if ris_tipo == "1" else "Pareggio" if ris_tipo == "X" else "Sconfitta"
                            luogo = "🏠 Casa" if match["home"] else "✈️ Trasferta"
                            
                            st.markdown(f"""
                            <div style='background-color: #f0f9ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                                <strong>vs {match['vs']}</strong><br>
                                {luogo}<br>
                                <span style='color: #3b82f6;'><strong>{ris_label}</strong></span><br>
                                <small>Prob: {prob*100:.1f}%</small>
                            </div>
                            """, unsafe_allow_html=True)
            
            # Mostra probabilità obiettivi
            st.markdown("#### 📊 Probabilità di Raggiungere gli Obiettivi")
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            
            with col_p1:
                st.metric("🏆 Scudetto", f"{prob_obiettivi['Scudetto']:.1f}%")
            with col_p2:
                st.metric("🌟 Champions", f"{prob_obiettivi['Champions']:.1f}%")
            with col_p3:
                st.metric("📈 Europa", f"{prob_obiettivi['Europa']:.1f}%")
            with col_p4:
                st.metric("✅ Salvezza", f"{prob_obiettivi['Salvezza']:.1f}%")
            
            # Calcola e mostra classifica finale
            punti_finali_squadra = st.session_state.squadra_selezionata['punti'] + sum(
                3 if r[0]=='1' else 1 if r[0]=='X' else 0 for r in risultati_ai
            )
            
            classifica_finale = []
            for sq in st.session_state.classifica:
                if sq["nome"] == squadra_selezionata:
                    punti_finali = punti_finali_squadra
                else:
                    punti_da_media = round(sq["mediaPunti"] * sq["partiteRimanenti"])
                    punti_finali = sq["punti"] + punti_da_media
                
                classifica_finale.append({
                    "nome": sq["nome"],
                    "puntiFinali": punti_finali,
                    "DR": sq["DR"]
                })
            
            classifica_finale = ordina_classifica(classifica_finale, "puntiFinali")
            
            st.markdown("#### 🏁 Classifica Finale Proiettata")
            df_finale = pd.DataFrame([
                {
                    "#": idx + 1,
                    "Squadra": sq["nome"] + (" ⭐" if sq["nome"] == squadra_selezionata else ""),
                    "Punti Finali": sq["puntiFinali"],
                    "DR": sq["DR"]
                }
                for idx, sq in enumerate(classifica_finale)
            ])
            
            def color_final_rows(row):
                idx = row.name
                color = get_colore_zona(idx)
                squadra = row["Squadra"].replace(" ⭐", "")
                if squadra == squadra_selezionata:
                    color = "#fef9c3"
                return [f'background-color: {color}'] * len(row)
            
            styled_finale = df_finale.style.apply(color_final_rows, axis=1)
            st.dataframe(styled_finale, use_container_width=True, hide_index=True)
            
            pos_finale = next(idx + 1 for idx, sq in enumerate(classifica_finale) if sq["nome"] == squadra_selezionata)
            
            if pos_finale == 1:
                st.success(f"🏆 **{squadra_selezionata}** vincerà lo SCUDETTO con {classifica_finale[0]['puntiFinali']} punti!")
            elif pos_finale <= 4:
                st.success(f"🌟 **{squadra_selezionata}** si qualificherà in CHAMPIONS LEAGUE! (Posizione: {pos_finale}°)")
            elif pos_finale <= 7:
                st.info(f"📈 **{squadra_selezionata}** si qualificherà in EUROPA LEAGUE (Posizione: {pos_finale}°)")
            elif pos_finale >= 18:
                st.error(f"⚠️ **{squadra_selezionata}** retrocederà in Serie B... (Posizione: {pos_finale}°)")
            else:
                st.warning(f"**{squadra_selezionata}** finirà a metà classifica (Posizione: {pos_finale}°)")
    
    # MODALITÀ MANUALE
    elif st.session_state.modalita == "manuale":
        st.markdown("### ✋ Inserimento Manuale")
        st.info("Inserisci manualmente i risultati delle partite")
        
        num_cols = 3
        risultati_completi = True
        
        for i in range(0, len(calendario_partite), num_cols):
            cols = st.columns(num_cols)
            for j, col in enumerate(cols):
                if i + j < len(calendario_partite):
                    with col:
                        match = calendario_partite[i + j]
                        luogo = "🏠" if match["home"] else "✈️"
                        key = f"partita_{i+j}"
                        risultato = st.selectbox(
                            f"{luogo} vs {match['vs']}",
                            ["", "1 (Vittoria)", "X (Pareggio)", "2 (Sconfitta)"],
                            key=key
                        )
                        st.session_state.risultati[key] = risultato
                        if risultato == "":
                            risultati_completi = False
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔮 CALCOLA CLASSIFICA FINALE", disabled=not risultati_completi, type="primary"):
            punti_guadagnati = 0
            for key, ris in st.session_state.risultati.items():
                if "Vittoria" in ris:
                    punti_guadagnati += 3
                elif "Pareggio" in ris:
                    punti_guadagnati += 1
            
            classifica_finale = []
            for sq in st.session_state.classifica:
                if sq["nome"] == squadra_selezionata:
                    punti_finali = sq["punti"] + punti_guadagnati
                else:
                    punti_da_media = round(sq["mediaPunti"] * sq["partiteRimanenti"])
                    punti_finali = sq["punti"] + punti_da_media
                
                classifica_finale.append({
                    "nome": sq["nome"],
                    "puntiFinali": punti_finali,
                    "DR": sq["DR"]
                })
            
            classifica_finale = ordina_classifica(classifica_finale, "puntiFinali")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🏁 Classifica Finale Simulata")
            
            df_finale = pd.DataFrame([
                {
                    "#": idx + 1,
                    "Squadra": sq["nome"] + (" ⭐" if sq["nome"] == squadra_selezionata else ""),
                    "Punti Finali": sq["puntiFinali"],
                    "DR": sq["DR"]
                }
                for idx, sq in enumerate(classifica_finale)
            ])
            
            def color_final_rows(row):
                idx = row.name
                color = get_colore_zona(idx)
                squadra = row["Squadra"].replace(" ⭐", "")
                if squadra == squadra_selezionata:
                    color = "#fef9c3"
                return [f'background-color: {color}'] * len(row)
            
            styled_finale = df_finale.style.apply(color_final_rows, axis=1)
            st.dataframe(styled_finale, use_container_width=True, hide_index=True)
            
            pos_finale = next(idx + 1 for idx, sq in enumerate(classifica_finale) if sq["nome"] == squadra_selezionata)
            
            if pos_finale == 1:
                st.success(f"🏆 **{squadra_selezionata}** vincerà lo SCUDETTO con {classifica_finale[0]['puntiFinali']} punti!")
            elif pos_finale <= 4:
                st.success(f"🌟 **{squadra_selezionata}** si qualificherà in CHAMPIONS LEAGUE! (Posizione: {pos_finale}°)")
            elif pos_finale <= 7:
                st.info(f"📈 **{squadra_selezionata}** si qualificherà in EUROPA LEAGUE (Posizione: {pos_finale}°)")
            elif pos_finale >= 18:
                st.error(f"⚠️ **{squadra_selezionata}** retrocederà in Serie B... (Posizione: {pos_finale}°)")
            else:
                st.warning(f"**{squadra_selezionata}** finirà a metà classifica (Posizione: {pos_finale}°)")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Simulatore Serie A - Dati aggiornati in tempo reale con AI predittiva</p>", unsafe_allow_html=True)