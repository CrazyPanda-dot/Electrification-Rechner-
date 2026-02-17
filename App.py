import streamlit as st

st.set_page_config(page_title="Fair-Vergleich: Solo vs. XTR2", page_icon="⚖️")

st.title("⚖️ Der 'Äpfel mit Äpfeln' Vergleich")
st.markdown("Unterscheidung zwischen **reiner Testzeit** und **Test + Doku**.")

# --- Sidebar Eingaben ---
st.sidebar.header("⚙️ Parameter")
anzahl_melder = st.sidebar.number_input("Melder pro Jahr", value=2000, step=100)
stundensatz = st.sidebar.number_input("Techniker-Stundensatz (€)", value=65)
kombi_anteil = st.sidebar.slider("Anteil Kombimelder (%)", 0, 100, 30)

st.sidebar.divider()
st.sidebar.subheader("Solo Parameter")
zeit_solo_test = st.sidebar.number_input("Nur Testzeit (Min/Melder)", value=3.0, help="Reine Zeit an der Leiter")
zeit_solo_doku = st.sidebar.number_input("Zusatzzeit Doku (Min/Melder)", value=2.5, help="Excel tippen, Listen abgleichen")

# --- Logik ---
# XTR2 Fixwerte
zeit_xtr_test = 2.5  # Inkl. Hitze-Automatik
zeit_xtr_doku = 0.2  # Nur App-Bestätigung/Synchronisation
invest_diff = 1500
cloud_jahr = 282

# Kosten-Berechnung Solo
# Norm-Zuschlag für Hitze beim Solo (ca. 3 Min extra pro Kombimelder)
extra_zeit_hitze_solo = (anzahl_melder * (kombi_anteil/100) * 3) / 60

stunden_solo_rein = (anzahl_melder * zeit_solo_test / 60) + extra_zeit_hitze_solo
stunden_solo_doku = (anzahl_melder * zeit_solo_doku / 60)

kosten_solo_rein = stunden_solo_rein * stundensatz + (anzahl_melder/150 * 17)
kosten_solo_mit_doku = (stunden_solo_rein + stunden_solo_doku) * stundensatz + (anzahl_melder/150 * 17)

# Kosten-Berechnung XTR2
stunden_xtr_rein = (anzahl_melder * zeit_xtr_test / 60)
stunden_xtr_doku = (anzahl_melder * zeit_xtr_doku / 60)

kosten_xtr_rein = stunden_xtr_rein * stundensatz + (anzahl_melder/600 * 42) + cloud_jahr
kosten_xtr_mit_doku = (stunden_xtr_rein + stunden_xtr_doku) * stundensatz + (anzahl_melder/600 * 42) + cloud_jahr

# --- Darstellung ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Reine Prüfzeit")
    st.write("*(An der Leiter, ohne Büro)*")
    diff_rein = kosten_solo_rein - kosten_xtr_rein
    st.metric("Ersparnis", f"{diff_rein:,.2f} €", delta=f"{diff_rein/anzahl_melder:.2f} €/Melder")

with col2:
    st.subheader("2. Gesamtprozess")
    st.write("*(Inkl. Excel/Protokoll)*")
    diff_doku = kosten_solo_mit_doku - kosten_xtr_mit_doku
    st.metric("Ersparnis", f"{diff_doku:,.2f} €", delta=f"{diff_doku/anzahl_melder:.2f} €/Melder", delta_color="normal")

st.divider()

# ROI Visualisierung
st.write("### Wann lohnt sich der Wechsel?")
option = st.radio("Berechnungsgrundlage für Amortisation:", ("Reine Prüfzeit", "Gesamtprozess"))

aktuelle_ersparnis = diff_rein if option == "Reine Prüfzeit" else diff_doku

if aktuelle_ersparnis > 0:
    amort_melder = int(invest_diff / (aktuelle_ersparnis / anzahl_melder))
    st.success(f"**Ergebnis:** Bei Fokus auf '{option}' amortisiert sich der XTR2 nach **{amort_melder} Meldern**.")
else:
    st.warning("In diesem Szenario ist der XTR2 teurer als das Solo-System.")

st.caption("Hinweis: Beim Solo-System wird bei Kombimeldern ein Zeitaufschlag für den normgerechten Hitzetest (Gerätewechsel) berechnet.")
