import streamlit as st
import requests

# ----------------------- CONFIGURATION PAGE -----------------------
st.set_page_config(page_title="Analyseur GitHub", page_icon="🐙", layout="wide")

# ----------------------- STYLE CSS PERSONNALISÉ -------------------
st.markdown("""
<style>
    .big-avatar img {
        border-radius: 20px;
        border: 3px solid #FFBB33;
        box-shadow: 0px 4px 10px rgba(255,187,51,0.4);
    }
    
    .info-card {
        background: #111;
        padding: 20px;
        border-radius: 20px;
        color: white;
        border: 1px solid #333;
    }
    
    .stat-box {
        background: #222;
        padding: 12px 18px;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
        color: #FFBB33;
        font-weight: 600;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------- TITRE -----------------------
st.title("🐙 Analyseur de Profil GitHub — Ultra Moderne")

st.markdown("""
Bienvenue dans **l’Analyseur GitHub**, un outil moderne et professionnel conçu pour examiner un profil GitHub en un seul clic.  
Grâce à cette application, vous pouvez :

🔍 **Rechercher un utilisateur GitHub**  
📊 **Consulter ses statistiques principales** : followers, repos, contributions  
📁 **Explorer ses meilleurs dépôts**  
🎨 **Profiter d’une interface élégante, sombre et moderne**

Cette plateforme a été pensée pour les développeurs, étudiants, recruteurs et passionnés souhaitant analyser rapidement l’activité d’un profil GitHub avec style et précision.

---
""")

# ----------------------- INPUT -----------------------
username = st.text_input("🔎 Entrez un pseudo GitHub :", "")

if st.button("Analyser le Profil"):
    if username == "":
        st.warning("⚠️ Veuillez entrer un pseudo.")
    else:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # ----------------------- LAYOUT EN COLONNES -----------------------
            col1, col2 = st.columns([1, 2])

            # ----------------------- AVATAR -----------------------
            with col1:
                st.markdown(
                    f"<div class='big-avatar'>"
                    f"<img src='{data['avatar_url']}' width='330'/>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("### 🔗 Profils sociaux")
                st.markdown(f"- 🌐 **GitHub** : [{data.get('html_url')}]({data.get('html_url')})")

            # ----------------------- INFORMATIONS -----------------------
            with col2:
                st.markdown("<div class='info-card'>", unsafe_allow_html=True)

                st.markdown(f"## {data.get('name','Nom non renseigné')}")
                st.markdown(f"### @{data.get('login')}")
                st.write(data.get("bio", "Aucune biographie."))

                st.write("---")

                # ----------------------- STATS -----------------------
                sc1, sc2, sc3 = st.columns(3)
                sc1.markdown(f"<div class='stat-box'>👥 Followers<br>{data['followers']}</div>", unsafe_allow_html=True)
                sc2.markdown(f"<div class='stat-box'>👤 Following<br>{data['following']}</div>", unsafe_allow_html=True)
                sc3.markdown(f"<div class='stat-box'>📦 Repos<br>{data['public_repos']}</div>", unsafe_allow_html=True)

                st.write("---")

                st.markdown(f"📍 **Localisation :** {data.get('location','Non spécifiée')}")
                st.markdown(f"🏢 **Entreprise :** {data.get('company','Non spécifiée')}")
                st.markdown(f"📧 **Email :** {data.get('email','Non disponible')}")

                st.markdown("</div>", unsafe_allow_html=True)

            # ----------------------- TOP REPOS -----------------------
            st.write("##  Répertoires les plus populaires")
            repos_url = data["repos_url"]
            repos = requests.get(repos_url).json()
            repos_sorted = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)

            for repo in repos_sorted[:5]:
                st.markdown(
                    f"""
                    <div style="background:#111;padding:15px;border-radius:15px;margin-bottom:10px;border:1px solid #333;">
                        <h4 style="color:#FFBB33;">{repo['name']}</h4>
                        ⭐ {repo['stargazers_count']} — 🍴 {repo['forks_count']}  
                        <br>
                        <a href="{repo['html_url']}">🔗 Voir le repo</a>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.error("❌ Utilisateur introuvable.")
