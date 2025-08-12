# This is the project's README file with setup instructions.

# University Course Recommender Backend

This is the backend for the University Course Recommender System, implemented with Python, Flask, and Firestore.

### Setup Instructions

1.  **Firebase Project:** Create a new Firebase project and enable Firestore.
2.  **Service Account:** In your Firebase project settings, go to "Service accounts" and click "Generate new private key". Rename the downloaded JSON file to `firebase-sa.json` and place it in the same directory as `main.py`.
3.  **Database Seeding:** Populate your Firestore database with `courses` and `degrees` collections. The structure should match the one assumed by the Python code.
4.  **Install Dependencies:** Run `pip install -r requirements.txt`.
5.  **Run the Server:** Run `python main.py`.

The server will be available at `http://localhost:5000`. You can now use the provided API endpoints to interact with the system.

# --- File: firebase-sa.json ---
# You need to create this file yourself.
# This file contains the JSON key for your Firebase service account.
# Place the content you downloaded from Firebase into this file.
# The content will look something like this:
# {
#   "type": "service_account",
#   "project_id": "your-project-id",
#   "private_key_id": "...",
#   "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
#   "client_email": "...",
#   "client_id": "...",
#   "auth_uri": "...",
#   "token_uri": "...",
#   "auth_provider_x509_cert_url": "...",
#   "client_x509_cert_url": "..."
# }
