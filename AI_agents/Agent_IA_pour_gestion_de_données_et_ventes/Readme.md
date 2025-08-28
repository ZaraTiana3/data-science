# 🤖 Agent IA pour la gestion de données et ventes

## 📌 Description
Ce projet met en place un **assistant intelligent** pour gérer et analyser les ventes à partir d’une base de données produits.  
Il combine **LangChain**, **Streamlit** et des outils **MCP** afin de :  
- Automatiser le suivi des stocks  
- Calculer automatiquement prix de revient, prix de vente et bénéfices  
- Fournir une interface simple pour interagir avec les données
- Mémoire vectorielle pour contextualiser les requêtes utilisateur

---

## 🛠️ Technologies utilisées
- **LangChain** pour la création de l'agent IA  
- **Streamlit** pour l' interface utilisateur  
- **MCP (Model Context Protocol)** pour les outils mcp et la création de serveur mcp personnalisé 
- **Docker** :
  - `ankane/pgvector` pour le  stockage vectoriel pour la mémorisation  
  - `postgresmcp` pour la gestion automatisée de la base de données  
- **Python** (project_tools.py) pour  outils de calcul et mémoire

---


## 🚀 Installation et exécution

### 1. Cloner le projet
```bash
git clone https://github.com/toncompte/nom_du_repo.git
cd nom_du_repo'
```
### 2.Lancer les services Docker
Démarre la base de données Postgres avec extension pgvector et postgresmcp :
```bash
docker compose up -d
```

### 3. Installer les dépendances Python
Crée un environnement virtuel puis installe les librairies :
```bash
python -m venv venv
source venv/bin/activate   # sous Linux/Mac
venv\Scripts\activate      # sous Windows
pip install -r requirements.txt
```

### 4. Lancer l’application
```bash
python project_tools.py     #pour lancer le serveur mcp
streamlit run app.py
```

## 🔮 Améliorations prévues
- Visualisations avancées (ventes par catégorie, marges mensuelles, etc.)
- Ajout d’alertes automatiques (ex. seuils de stock critiques)



