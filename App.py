import streamlit as st

st.set_page_config(page_title="XTR2 Profit-Rechner", page_icon="📈")

# Titel und Einleitung
st.title("📈 ROI-Rechner: Modernisierung der Brandmelderprüfung")
st.markdown("""
Vergleich zwischen dem **Standard-Verfahren (Solo A5 Aerosol)** und der **digitalen Prüfung (Testifire XTR2)**.
Dieser Rechner berücksichtigt den Personalwechsel (2-Mann vs. 1-Mann) und die Cloud-Anbindung.
""")

# --- EINGABE-BEREICH ---
st.header("1. Projekt-Parameter")
col1, col2 = st.columns(2)

with col1:
    anzahl_melder = st.number_input("Anzahl Melder pro Jahr", value=2000, step=100)
    stundensatz = st.number_input("Stundensatz pro Techniker (€)", value=65)
    kombi_anteil = st.slider("Anteil Kombimelder (Rauch/Wärme) in %", 0, 100, 30)

with col2:
    preis_a5 = st.number_input("Preis Solo A5 Dose (€)", value=17.0)
    preis_ts3 = st.number_input("Preis TS3 Kapsel (€)", value=42.0)
    invest_diff = st.number_input("Mehrpreis XTR2 System (einmalig €)", value=1500)

st.divider()

# --- SZENARIO-KONFIGURATION ---
st.header("2. Prozess-Einstellungen")
doku_aktiv = st.checkbox("Dokumentationsaufwand (Excel/Papier) einbeziehen?", value=True)

with st.expander("Detaillierte Zeit-Einstellungen (Sekunden/Minuten)"):
    c_s, c_x = st.columns(2)
    with c_s:
        st.markdown("**Solo A5 (2-Mann-Team)**")
        sek_s_test = st.number_input("Reine Sprühzeit (Sek)", value=30)
        min_s_ruest = st.number_input("Rüstzeit pro Melder (Min)", value=2.0)
        min_s_doku = st.number_input("Doku pro Melder (Min)", value=2.5)
        st.caption("Hinweis: Lohnkosten werden x2 gerechnet (1x Melder, 1x BMZ).")
    
    with c_x:
        st.markdown("**XTR2 (1-Mann-Team)**")
        sek_x_test = st.number_input("Test inkl. Freiblasen (Sek)", value=20)
        min_x_ruest = st.number_input("Rüstzeit pro Melder (Min)", value=1.8)
        min_x_doku = st.number_input("Doku pro Melder (Min)", value=0.2)
        st.caption("Hinweis: BMZ-Reset erfolgt direkt durch den Techniker via App.")

# --- KALKULATIONS-LOGIK ---

# 1. Materialkosten (Basierend auf Solo A5 @ 150 Tests & TS3 @ 600 Tests)
material_s = (anzahl_melder / 150) * preis_a5
material_x = (anzahl_melder / 600) * preis_ts3
cloud_xtr = 282.0 # Jährliche Cloud-Gebühr

# 2. Zeitberechnung für Kombimelder (Zwei separate Alarme nötig)
# Solo: Muss Kopf tauschen, BMZ-Reset durch 2. Mann, 2x Rüstzeit
t_solo_kombi = (sek_s_test/60) + (30/60) + (2 * min_s_ruest) + 3.5 + 2.0 # 3.5 Min Kopfwechsel, 2 Min Kommunikation
# XTR2: Stange bleibt oben, BMZ-Reset via App, Rauch & Hitze nacheinander
t_xtr_kombi = (sek_x_test/60) + (20/60) + min_x_ruest + 1.0 # 1 Min App-Handling

# 3. Stunden-Kalkulation (Gewichtung Standard vs. Kombi)
if doku_aktiv:
    # Solo Stunden (Feldzeit + Doku)
    h_s_std = (anzahl_melder * (1 - kombi_anteil/100) * (sek_s_test/60 + min_s_ruest + min_s_doku)) / 60
    h_s_kombi = (anzahl_melder * (kombi_anteil/100) * (t_solo_kombi + min_s_doku)) / 60
    # XTR2 Stunden (Feldzeit + Doku)
    h_x_std = (anzahl_melder * (1 - kombi_anteil/100) * (sek_x_test/60 + min_x_ruest + min_x_doku)) / 60
    h_x_kombi = (anzahl_melder * (kombi_anteil/100) * (t_xtr_kombi + min_x_doku)) / 60
else:
    h_s_std = (anzahl_melder * (1 - kombi_anteil/100) * (sek_s_test/60 + min_s_ruest)) / 60
    h_s_kombi = (anzahl_melder * (kombi_anteil/100) * t_solo_kombi) / 60
    h_x_std = (anzahl_melder * (1 - kombi_anteil/100) * (sek_x_test/60 + min_x_ruest)) / 60
    h_x_kombi = (anzahl_melder * (kombi_anteil/100) * t_xtr_kombi) / 60

stunden_solo_jahr = h_s_std + h_s_kombi
stunden_xtr_jahr = h_x_std + h_x_kombi

# 4. Gesamtkosten (Lohn Solo x 2 Techniker vs. XTR2 x 1 Techniker)
lohnkosten_solo = stunden_solo_jahr * (stundensatz * 2)
lohnkosten_xtr = stunden_xtr_jahr * stundensatz

total_solo = lohnkosten_solo + material_s
total_xtr = lohnkosten_xtr + material_x + cloud_xtr

ersparnis = total_solo - total_xtr

# --- ERGEBNIS-ANZEIGE ---
st.divider()
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.subheader("Solo A5 (Standard)")
    st.metric("Gesamtkosten / Jahr", f"{total_solo:,.2f} €")
    st.write(f"Techniker-Stunden: {stunden_solo_jahr * 2:.1f} (Team)")

with res_col2:
    st.subheader("Testifire XTR2")
    st.metric("Gesamtkosten / Jahr", f"{total_xtr:,.2f} €")
    st.write(f"Techniker-Stunden: {stunden_xtr_jahr:.1f} (Ein-Mann)")

st.divider()

if ersparnis > 0:
    st.success(f"### Jährliche Ersparnis: {ersparnis:,.2f} €")
    ersparnis_pro_melder = ersparnis / anzahl_melder
    roi_melder = int(invest_diff / ersparnis_pro_melder)
    st.info(f"💡 **Amortisation:** Der XTR2 hat sich nach bereits **{roi_melder} geprüften Meldern** vollständig bezahlt gemacht.")
    
    # Kapazitäts-Bonus
    freigewordene_stunden = (stunden_solo_jahr * 2) - stunden_xtr_jahr
    st.warning(f"🚀 **Kapazitäts-Gewinn:** Deine Techniker gewinnen **{freigewordene_stunden:.1f} Arbeitsstunden** pro Jahr für andere Projekte!")
else:
    st.error("In diesem Szenario übersteigen die XTR2-Kosten das aktuelle System.")
