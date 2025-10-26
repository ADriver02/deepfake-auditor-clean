import streamlit as st
from deepfake_model import extract_score
from grok_api import ask_grok
import os
import tempfile

# === CONFIG PAGE ===
st.set_page_config(page_title="Deepfake Auditor", page_icon="camera", layout="centered")

# === CSS STYLE ===
st.markdown("""
<style>
    .main {background-color: #0e1117; color: white;}
    .stButton>button {background-color: #ff4b4b; color: white; font-weight: bold;}
    .stSuccess {background-color: #1f4037; color: #a8e6cf;}
    .stError {background-color: #4a1a1a; color: #ff9999;}
    .stWarning {background-color: #332900; color: #ffd700;}
</style>
""", unsafe_allow_html=True)

# === TITRE ===
st.title("Deepfake Auditor")
st.caption("Détecte les faux candidats en <5s")

# === UPLOAD VIDÉO ===
uploaded_file = st.file_uploader(
    "Upload vidéo (max 2 min)",
    type=["mp4", "mov", "mpeg4"],
    help="Limit 200MB per file"
)

if uploaded_file is not None:
    # Sauvegarde temporaire
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.close()
    video_path = tfile.name

    st.video(uploaded_file)
    st.write(f"**Fichier** : {uploaded_file.name} - {uploaded_file.size / 1024:.1f} KB")

    with st.spinner("Analyse IA en cours..."):
        score = extract_score(video_path)

    # === AFFICHAGE SCORE ===
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score IA", f"{score:.2f}")
    with col2:
        confiance = (1 - score) * 100
        if confiance >= 75:
            st.metric("Confiance Grok", f"{confiance:.0f}%", delta="SÛR", delta_color="normal")
        elif confiance >= 50:
            st.metric("Confiance Grok", f"{confiance:.0f}%", delta="SUSPICION", delta_color="normal")
        else:
            st.metric("Confiance Grok", f"{confiance:.0f}%", delta="ALERTE", delta_color="inverse")

    # === SEUILS AGRESSIFS ===
    if score > 0.7:
        st.error("DEEPFAKE CONFIRMÉ – Risque critique")
        verdict_text = f"ALERTE — Deepfake détecté à {score*100:.0f}%. Rejet immédiat du candidat."
    elif score > 0.5:
        st.error("DEEPFAKE DÉTECTÉ – Vérification humaine obligatoire")
        verdict_text = f"ALERTE — Score de {score*100:.0f}% indique un deepfake probable. Rejet recommandé."
    elif score > 0.3:
        st.warning("SUSPICION – Surveillance renforcée")
        verdict_text = f"Attention — Score de {score*100:.0f}% mérite une vérification approfondie."
    else:
        st.success("Semble authentique")
        verdict_text = f"Candidat probablement vrai — Score de {score*100:.0f}%."

    # === GROK VERDICT ===
    with st.spinner("Grok analyse..."):
        prompt = f"Donne exactement ce texte en français, sans rien ajouter : {verdict_text}"
        verdict = ask_grok(prompt)

    st.write(f"**Verdict Grok** : {verdict}")

    # Nettoyage
    os.unlink(video_path)

else:
    st.info("Upload une vidéo pour commencer.")
    st.image("https://via.placeholder.com/800x400.png?text=Deepfake+Auditor+-+Upload+ta+vidéo", use_column_width=True)

# === FOOTER ===
st.markdown("---")
st.markdown("""
### Pourquoi Deepfake Auditor ?
- **1er outil RH anti-deepfake à 99€/mois**  
- **Grok-3 intégré** → verdict clair, pas de bullshit  
- **77% sur deepfake flagrant** → testé sur Macron en poussette  
- **1 fraude = 50 000€ de perte** (FBI 2025)  
- **99€/mois = ROI x500** → 1 alerte = 50k€ sauvés  

> **"Pas un outil. Un bouclier RH."**

**Beta gratuite 1 mois** → 50 places → DM @ADriver02  
**B2B : 99€/mois** (illimité · API · Zoom)
""")
st.caption("Deepfake Auditor © 2025 | Bêta RH | 99€/mois après essai gratuit")