# TP_CV_D2_20000_BDML2 — Streamlit CV + Course

**Étudiante :** YASSINE Yara — EFREI Paris — BDML2 — 2026-2027
**Cours :** STREAMLIT CV + Course - Dataset above
**Professeur :** MATHEW Mano Joseph (mano.mathew@efrei.fr)

Application Streamlit avec deux onglets :
1. **Mon CV (version fun)** : CV créatif (timeline interactive, projets en « quêtes », compétences, langues).
2. **Cours · TP DataViz NYC Taxi** : chargement, nettoyage, statistiques, visualisations dynamiques + KPI, storytelling.

## Lancer l'application

```bash
pip install -r requirements.txt
streamlit run app.py
```

Sous Windows, si les commandes ne sont pas reconnues :

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Le dataset est lu depuis l'URL du TP (kepler.gl) ; une copie locale (`data/data.csv`) sert de secours sans internet.


## Contenu

```
app.py                 application Streamlit
requirements.txt       dépendances
.streamlit/config.toml thème (couleurs)
assets/                photo, CV (PDF), logo EFREI à ajouter
data/data.csv          copie locale du dataset
notebook/              notebook du TP (DataViz_20000_YASSINE2026BDML2.ipynb)
```
