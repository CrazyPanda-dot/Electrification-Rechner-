import streamlit as st

st.set_page_config(page_title="ROI: Solo A5 vs. XTR2", page_icon="⚖️")

st.title("⚖️ Wirtschaftlichkeits-Check")
st.markdown("Vergleich: **Solo A5 Aerosol** vs. **Testifire XTR2**")

# --- EINGABEN ---
with st.expander("🛠️ Parameter anpassen", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        anzahl_melder = st.number_input("Melder pro Jahr", value=2000, step=100)
        stundensatz = st.number_input("Stundensatz Techniker (€)", value=65)
        kombi_anteil = st.slider("Anteil Kombimelder (%)", 0, 100, 30)
    with col2:
        preis_a5 = st.number_input("Preis Solo A5 Dose (€)", value=17.0)
        preis_xtr = st.number_input("Preis TS3 Kapsel (€)", value=42.0)
        invest_diff = st.number_input("Mehrpreis XTR2 System (€)", value=1500)

# --- KALKULATIONS-LOGIK ---
# Daten-Basis aus deinen Files & Vorgaben:
yield_a5 = 150  # Tests pro Dose Solo A5
yield_xtr = 600 # Konservative Einstellung für TS3 Kapsel

# Zeit-Faktoren (in Minuten)
sek_solo_test = 30 / 60
sek_xtr_test = 20 / 60
zeit_wechsel_solo = 3.5  # Mehraufwand für Hitze-Test (Kopfwechsel)
zeit_doku_solo = 2.5     # Manuelle Doku/Excel
zeit_doku_xtr = 0.2      # Digitaler Sync

# Berechnung Solo A5
stunden_solo_feld = (anzahl_melder * sek_solo_test / 60) + (anzahl_melder * (kombi_anteil/100) * zeit_wechsel_solo / 60)
stunden_solo_doku = (anzahl_melder * zeit_doku_solo / 60)
material_solo = (anzahl_melder / yield_a5) * preis_a5
gesamt_solo = (stunden_solo_feld + stunden_solo_doku) * stundensatz + material_solo

# Berechnung XTR2
stunden_xtr_feld = (anzahl_melder * sek_xtr_test / 60)
stunden_xtr_doku = (anzahl_melder * zeit_doku_xtr / 60)
material_xtr = (anzahl_melder / yield_xtr) * preis_xtr
cloud_jahr = 282.0
gesamt_xtr = (stunden_xtr_feld + stunden_xtr_doku) * stundensatz + material_xtr + cloud_jahr

# Ergebnisse
ersparnis = gesamt_solo - gesamt_xtr
ersparnis_pro_melder = ersparnis / anzahl_melder if anzahl_melder > 0 else 0

# --- AUSGABE ---
st.divider()
c1, c2 = st.columns(2)
c1.metric("Kosten Solo A5 / Jahr", f"{gesamt_solo:,.2f} €")
c2.metric("Kosten XTR2 / Jahr", f"{gesamt_xtr:,.2f} €")

st.success(f"### Ersparnis pro Jahr: {ersparnis:,.2f} €")

if ersparnis > 0:
    roi_melder = int(invest_diff / ersparnis_pro_melder)
    st.info(f"**Amortisation:** Das System ist nach **{roi_melder} Meldern** bezahlt.")

with st.expander("Details zur Verbrauchs-Matrix"):
    st.write(f"**Verbrauch Solo A5:** {anzahl_melder/yield_a5:.1f} Dosen p.a.")
    st.write(f"**Verbrauch XTR2 TS3:** {anzahl_melder/yield_xtr:.1f} Kapseln p.a.")
    st.write(f"**Zeitvorteil:** XTR2 spart ca. {(stunden_solo_feld + stunden_solo_doku) - (stunden_xtr_feld + stunden_xtr_doku):.1f} Arbeitsstunden pro Jahr.")
