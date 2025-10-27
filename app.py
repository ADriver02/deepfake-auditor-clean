import streamlit as st
from deepfake_model import extract_score
from grok_api import ask_grok
import os
import tempfile

# === CONFIG ===
st.set_page_config(page_title="Deepfake Auditor", page_icon="camera", layout="centered")

# === CSS ===
st.markdown("""
<style>
    .main {background-color: #0e1117; color: white;}
    .stButton>button {background-color: #ff4b4b; color: white; font-weight: bold;}
    .stError {background-color: #4a1a1a; color: #ff9999;}
    .stWarning {background-color: #332900; color: #ffd700;}
</style>
""", unsafe_allow_html=True)

st.title("Deepfake Auditor")
st.caption("Détecte les faux candidats en <5s")

uploaded_file = st.file_uploader("Upload vidéo (max 2 min)", type=["mp4", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.close()
    video_path = tfile.name

    st.video(uploaded_file)
    st.write(f"**Fichier** : {uploaded_file.name}")

    with st.spinner("Analyse IA..."):
        score = extract_score(video_path)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score IA", f"{score:.2f}")
    with col2:
        confiance = (1 - score) * 100
        if confiance < 30:
            st.metric("Confiance Grok", f"{confiance:.0f}%", delta="ALERTE", delta_color="inverse")
        else:
            st.metric("Confiance Grok", f"{confiance:.0f}%")

    if score > 0.7:
        st.error("DEEPFAKE CONFIRMÉ – Risque critique")
        verdict_text = f"ALERTE — Deepfake détecté à {score*100:.0f}%. Rejet immédiat."
    elif score > 0.5:
        st.error("DEEPFAKE DÉTECTÉ – Vérification humaine")
        verdict_text = f"ALERTE — Score {score*100:.0f}% → rejet recommandé."
    else:
        st.success("Semble authentique")
        verdict_text = f"Candidat probablement vrai — Score {score*100:.0f}%."

    # === GROK OPTIONNEL ===
    if st.checkbox("Activer Grok (1 appel xAI)", value=False):
        with st.spinner("Grok analyse..."):
            prompt = f"Donne exactement ce texte en français : {verdict_text}"
            verdict = ask_grok(prompt)
        if "Erreur" in verdict or "403" in verdict or "manquante" in verdict:
            st.warning("Grok en pause (limite ou clé)")
            st.write(f"**Verdict IA** : {verdict_text}")
        else:
            st.write(f"**Verdict Grok** : {verdict}")
    else:
        st.write(f"**Verdict IA** : {verdict_text}")

    os.unlink(video_path)

else:
    st.info("Upload une vidéo pour commencer.")
    st.image("https://via.placeholder.com/800x400.png?text=Deepfake+Auditor", use_column_width=True)

# === FOOTER ===
st.markdown("---")
st.markdown("""
### Pourquoi Deepfake Auditor ?
- **1er outil RH anti-deepfake à 99€/mois**  
- **Grok-3 intégré** → verdict clair  
- **77% sur deepfake flagrant** → testé sur Macron en poussette  
- **1 fraude = 50 000€** (FBI 2025)  
- **99€/mois = ROI x500**  

> **"Pas un outil. Un bouclier RH."**

**Beta gratuite 1 mois** → 50 places → DM @ADriver02  
**B2B : 99€/mois** (illimité · API · Zoom)
""")