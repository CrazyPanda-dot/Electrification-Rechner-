import streamlit as st

st.set_page_config(page_title="Pro-Check: Solo A5 vs. XTR2", page_icon="⚖️")

# Titel und Einleitung
st.title("⚖️ Wirtschaftlichkeits-Check")
st.markdown("Vergleich: **Solo A5 Aerosol** vs. **Testifire XTR2**")

# --- 1. SZEANRIO-AUSWAHL ---
st.subheader("1. Szenario wählen")
doku_einbeziehen = st.radio(
    "Soll die Zeit für die Dokumentation (Excel/Papier) berücksichtigt werden?",
    ("Ja, inkl. Dokumentationsaufwand", "Nein, nur reine Zeit vor Ort"),
    index=0
)

st.divider()

# --- 2. EINGABE-BEREICH ---
st.subheader("2. Parameter anpassen")
col1, col2 = st.columns(2)

with col1:
    anzahl_melder = st.number_input("Melder pro Jahr", value=2000, step=100)
    stundensatz = st.number_input("Stundensatz Techniker (€)", value=65)
    kombi_anteil = st.slider("Anteil Kombimelder (%)", 0, 100, 30)

with col2:
    preis_a5 = st.number_input("Preis Solo A5 Dose (€)", value=17.0)
    preis_xtr = st.number_input("Preis TS3 Kapsel (€)", value=42.0)
    invest_diff = st.number_input("Mehrpreis XTR2 System (€)", value=1500)

st.divider()

# --- 3. ZEIT-VARIABLEN ---
st.subheader("3. Zeit-Schätzung (Minuten pro Melder)")
col_time1, col_time2 = st.columns(2)

with col_time1:
    st.markdown("**Zeitaufwand Solo A5**")
    t_solo_test = st.number_input("Testzeit (Sekunden)", value=30, help="Reine Sprühzeit") / 60
