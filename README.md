# Hexagonal Architecture & GenAI

## Objectif

Conception d'une application web permettant à un utilisateur de discuter avec un chatbot basé sur une API d’IA générative (ex: [Cohere](https://cohere.com/))
L’application doit respecter les principes de l’architecture hexagonale (clean architecture) et permettre de gérer plusieurs conversations avec historique.

---

## Fonctionnalités

### 1. Chatbot conversationnel avec mémoire
- L’utilisateur peut envoyer des messages à un chatbot.
- Le chatbot répond en utilisant une API d’IA générative.
- L’historique de chaque conversation est conservé et affiché à l’utilisateur.

### 2. Gestion multi-conversations
- L’utilisateur peut démarrer une nouvelle conversation à tout moment.
- Chaque conversation possède un identifiant unique (GUID).
- L’utilisateur peut consulter l’historique d’une conversation existante.

### 3. Persistance
- L’historique des conversations doit être stocké de façon persistante (ex : fichiers JSON, base de données, etc.).

### 4. API RESTful
- Exposez des endpoints pour :
  - Créer une nouvelle conversation
  - Envoyer un message dans une conversation
  - Récupérer l’historique d’une conversation
  - Lister toutes les conversations existantes
  - Réinitialiser l’historique d’une conversation

### 5. Interface utilisateur web
- Proposez une interface web simple (ex : Streamlit, React, Flask, etc.) permettant :
  - De discuter avec le chatbot
  - De visualiser l’historique
  - De démarrer une nouvelle conversation

---

### 6. Plus

- Ajout de fonctionnalités avancées (personnalisation du prompt système, gestion des utilisateurs, etc.)
- Interface utilisateur améliorée
- Déploiement (Docker, cloud, etc.)
- Tests unitaires et integration
