
## 😷 Détection du port de masque facial avec VGG16 et MTCNN

## Description 
Ce projet met en place un modèle de **vision par ordinateur** pour détecter si une personne porte un masque facial ou non.  
Il s’appuie sur :  
- **MTCNN** pour la détection des visages  
- **VGG16** (réseau pré-entraîné) pour la classification (masque / sans masque)  

### Dataset
- Utilisé : [Face Mask Dataset](https://www.kaggle.com/datasets/omkargurav/face-mask-dataset)  
- Contient des images de visages **avec masque** et **sans masque**.  

### Étapes principales du projet  
1. **Prétraitement des images** :  
   - Redimensionnement (224x224), normalisation et encodage en tenseurs  
   - Génération des labels correspondants (masque / sans masque)  
2. **Séparation des données** :  
   - Train/Test split (80% entraînement, 20% test)  
3. **Augmentation des données** :  
   - Utilisation de `ImageDataGenerator` (rotation, translation, zoom, luminosité) pour améliorer la robustesse du modèle  
4. **Entraînement du modèle** :  
   - Réseau **VGG16** (transfer learning) adapté au dataset  
5. **Évaluation** :  
   - Prédiction sur le jeu de test  
6. **Sauvegarde du modèle** :  
   - Export du modèle entraîné pour une réutilisation future  

## 🎥 Détection en temps réel avec la webcam

En plus de l’entraînement et de l’évaluation du modèle, le projet inclut un script `detect_mask.py` permettant de tester la détection du port de masque en temps réel via la webcam de l’ordinateur.  

### Utilisation
Après sauvegarde du  modèle entraîné (`mask_detector_model.h5`), suivre ces étapes suivantes: 

#### Installer les dépendances Python
Crée un environnement virtuel puis installe les librairies :
```bash
python -m venv venv
source venv/bin/activate   # sous Linux/Mac
venv\Scripts\activate      # sous Windows
pip install -r requirements.txt
```

#### Lancer l’application
```bash
python detect_mask.py
```

