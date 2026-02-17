import streamlit as st

st.set_page_config(page_title="Präzisions-Check: Solo vs. XTR2", page_icon="⚖️")

# CSS für bessere mobile Lesbarkeit der Eingabefelder
st.markdown("""
    <style>
    .stNumberInput, .stSlider { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Zeit-Präzisions-Vergleich")

# --- EINGABE DIREKT AUF DER HAUPTSEITE ---
st.subheader("1. Deine Eckdaten")
col_a, col_b = st.columns(2)
with col_a:
    anzahl_melder = st.number_input("Melder pro Jahr", value=2000, step=100)
    stundensatz = st.number_input("Stundensatz (€)", value=65)
with col_b:
    kombi_anteil = st.slider("Kombimelder (%)", 0, 100, 30)
    invest_diff = st.number_input("Mehrpreis XTR2 Set (€)", value=1500)

st.divider()

st.subheader("2. Zeit-Parameter (Sekunden)")
col_c, col_d = st.columns(2)
with col_c:
    st.markdown("**Solo 330**")
    sek_solo_test = st.number_input("Sek. pro Test (Solo)", value=30, help="Reine Sprühzeit")
    min_solo_ruest = st.number_input("Rüstzeit (Min/Melder)", value=2.0, help="Leiter, Laufen, Positionieren")
    min_solo_doku = st.number_input("Doku (Min/Melder)", value=2.5, help="Excel/Papier nachpflegen")

with col_d:
    st.markdown("**Testifire XTR2**")
    sek_xtr_test = st.number_input("Sek. pro Test (XTR2)", value=20, help="Inkl. Freiblasen")
    min_xtr_ruest = st.number_input("Rüstzeit (Min/Melder)", value=1.8, help="Oft schneller durch geringeres Gewicht/Handling")
    min_xtr_doku = st.number_input("Doku (Min/Melder)", value=0.2, help="Automatischer Sync")

# --- LOGIK ---
# Zeit in Stunden umrechnen
# Solo: Testzeit + Rüstzeit + (bei Kombimeldern +3 Min für Gerätewechsel Hitze)
zeit_pro_melder_solo = (sek_solo_test / 60) + min_solo_ruest
extra_hitze_solo = (anzahl_melder * (kombi_anteil/100) * 3) / 60
stunden_solo_rein = (anzahl_melder * zeit_pro_melder_solo / 60) + extra_hitze_solo
stunden_solo_doku = (anzahl_melder * min_solo_doku / 60)

# XTR2: Testzeit + Rüstzeit (Hitze ist im Test inkludiert, kein Wechsel nötig)
zeit_pro_melder_xtr = (sek_xtr_test / 60) + min_xtr_ruest
stunden_xtr_rein = (anzahl_melder * zeit_pro_melder_xtr / 60)
stunden_xtr_doku = (anzahl_melder * min_xtr_doku / 60)

# Kosten
material_solo = (anzahl_melder / 150) * 17
kosten_solo_rein = (stunden_solo_rein * stundensatz) + material_solo
kosten_solo_doku = (stunden_solo_rein + stunden_solo_doku) * stundensatz + material_solo

material_xtr = (anzahl_melder / 600) * 42
kosten_xtr_rein = (stunden_xtr_rein * stundensatz) + material_xtr + 282
kosten_xtr_doku = (stunden_xtr_rein + stunden_xtr_doku) * stundensatz + material_xtr + 282

# --- AUSGABE ---
st.divider()
res_rein, res_doku = st.columns(2)

with res_rein:
    diff_r = kosten_solo_rein - kosten_xtr_rein
    st.metric("Ersparnis (Nur Feld)", f"{diff_r:,.2f} €")

with res_doku:
    diff_d = kosten_solo_doku - kosten_xtr_doku
    st.metric("Ersparnis (Inkl. Doku)", f"{diff_d:,.2f} €")

st.info(f"**Amortisation:** Bei Einbeziehung der Dokumentation rechnet sich das Gerät nach ca. **{int(invest_diff / (diff_d/anzahl_melder))} Meldern**.")
 
