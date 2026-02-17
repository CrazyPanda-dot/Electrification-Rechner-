import streamlit as st

# Seitenkonfiguration für Mobile
st.set_page_config(page_title="ROI Rechner: XTR2 vs. Solo", page_icon="🚀")

st.title("📊 Profit-Check: XTR2")
st.markdown("Vergleich: **Solo 330/461** vs. **Testifire XTR2**")

# --- Sidebar / Eingaben ---
st.header("Eingabewerte")

col1, col2 = st.columns(2)

with col1:
    anzahl_melder = st.number_input("Melder pro Jahr", value=2000, step=100)
    stundensatz = st.number_input("Stundensatz Techniker (€)", value=65)
    kombi_anteil = st.slider("Anteil Kombimelder (%)", 0, 100, 30)

with col2:
    preis_solo = st.number_input("Preis Solo Aerosol (€)", value=17.0)
    zeit_solo_basis = st.number_input("Zeit Solo (Min/Melder)", value=5.5, step=0.5)
    invest_diff = st.number_input("Mehrpreis XTR2 Set (€)", value=1500)

# --- Logik ---
# Solo Kalkulation
anzahl_kombi = anzahl_melder * (kombi_anteil / 100)
anzahl_standard = anzahl_melder - anzahl_kombi

# Zeit: Standard + 3 Min extra für Hitze bei Kombimeldern (Normgerecht)
zeit_gesamt_solo = (anzahl_standard * zeit_solo_basis) + (anzahl_kombi * (zeit_solo_basis + 3))
material_solo = (anzahl_melder / 150) * preis_solo
kosten_solo = material_solo + (zeit_gesamt_solo / 60) * stundensatz

# XTR2 Kalkulation
zeit_xtr = 2.5 # Konstant wegen Auto-Test & Digital-Protokoll
material_xtr = (anzahl_melder / 600) * 42.0
cloud_jahr = 282.0
kosten_xtr = material_xtr + (anzahl_melder * zeit_xtr / 60) * stundensatz + cloud_jahr

ersparnis = kosten_solo - kosten_xtr
ersparnis_pro_melder = ersparnis / anzahl_melder if anzahl_melder > 0 else 0

# --- Ausgabe ---
st.divider()

if ersparnis > 0:
    st.success(f"### Jährliche Ersparnis: {ersparnis:,.2f} €")
    
    amort_melder = int(invest_diff / ersparnis_pro_melder) if ersparnis_pro_melder > 0 else 0
    st.info(f"**Amortisation:** Das Gerät hat sich nach ca. **{amort_melder} Meldern** bezahlt gemacht.")
else:
    st.error("Bei diesen Werten ist das Solo-System günstiger.")

# --- Detail-Vergleich ---
with st.expander("Details anzeigen"):
    st.write(f"**Kosten Solo System:** {kosten_solo:,.2f} €")
    st.write(f"**Kosten XTR2 System:** {kosten_xtr:,.2f} €")
    st.caption("Basis: XTR2 mit 42€/Kapsel (600 Tests) und 2.5 Min Zeitaufwand inkl. Dokumentation.")
