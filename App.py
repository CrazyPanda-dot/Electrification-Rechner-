import streamlit as st

st.set_page_config(page_title="Rettung: Solo A5 vs. XTR2", page_icon="🚒")

# Titel
st.title("⚖️ Wirtschaftlichkeits-Check (Repariert)")
st.markdown("Vergleich: **Solo A5** vs. **Testifire XTR2**")

# --- 1. SZENARIO ---
st.subheader("1. Szenario wählen")
doku_aktiv = st.radio(
    "Dokumentationsaufwand einbeziehen?",
    ("Ja", "Nein"),
    index=0
)

# --- 2. BASISDATEN ---
st.divider()
st.subheader("2. Eckdaten")
col1, col2 = st.columns(2)
with col1:
    anzahl_melder = st.number_input("Melder pro Jahr", value=2000, step=100)
    stundensatz = st.number_input("Stundensatz (€)", value=65)
    kombi_anteil = st.slider("Kombimelder (%)", 0, 100, 30)
with col2:
    preis_a5 = st.number_input("Preis Solo A5 (€)", value=17.0)
    preis_xtr = st.number_input("Preis TS3 Kapsel (€)", value=42.0)
    invest_diff = st.number_input("Mehrpreis XTR2 (€)", value=1500)

# --- 3. ZEITEN ---
st.divider()
st.subheader("3. Zeit-Faktoren")
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Solo A5**")
    sek_s_test = st.number_input("Test (Sek)", value=30)
    min_s_ruest = st.number_input("Rüstzeit Solo (Min)", value=2.0)
    min_s_doku = st.number_input("Doku Solo (Min)", value=2.5)

with col4:
    st.markdown("**XTR2**")
    sek_x_test = st.number_input("Test (Sek)", value=20)
    min_x_ruest = st.number_input("Rüstzeit XTR2 (Min)", value=1.8)
    min_x_doku = st.number_input("Doku XTR2 (Min)", value=0.2)

# --- KALKULATION ---
# Materialkosten (basierend auf deinen Daten)
material_s = (anzahl_melder / 150) * preis_a5
material_x = (anzahl_melder / 600) * preis_xtr
cloud = 282.0

# Zeitberechnung (Umrechnung Sek in Min)
t_solo_base = (sek_s_test / 60) + min_s_ruest
t_xtr_base = (sek_x_test / 60) + min_x_ruest

# Zuschlag für Kombimelder (Solo Kopfwechsel)
t_extra_kombi_solo = (anzahl_melder * (kombi_anteil/100) * 3.5) / 60

if doku_aktiv == "Ja":
    h_solo = (anzahl_melder * (t_solo_base + min_s_doku) / 60) + t_extra_kombi_solo
    h_xtr = (anzahl_melder * (t_xtr_base + min_x_doku) / 60)
else:
    h_solo = (anzahl_melder * t_solo_base / 60) + t_extra_kombi_solo
    h_xtr = (anzahl_melder * t_xtr_base / 60)

# Gesamtsummen
kosten_s = (h_solo * stundensatz) + material_s
kosten_x = (h_xtr * stundensatz) + material_x + cloud

ersparnis = kosten_s - kosten_x

# --- AUSGABE ---
st.divider()
res1, res2 = st.columns(2)
res1.metric("Kosten Solo A5", f"{kosten_s:,.2f} €")
res2.metric("Kosten XTR2", f"{kosten_x:,.2f} €")

if ersparnis > 0:
    st.success(f"### Ersparnis: {ersparnis:,.2f} € / Jahr")
    ersparnis_pro_melder = ersparnis / anzahl_melder
    amort = int(invest_diff / ersparnis_pro_melder)
    st.info(f"Amortisation nach **{amort} Meldern**")
else:
    st.error("XTR2 ist in diesem Szenario teurer.")
