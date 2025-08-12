# Interactive DSA Course Recommender

This project is an interactive web application designed to help university students plan their courses. It leverages core Data Structures and Algorithms (DSA) concepts to provide intelligent features like course recommendations, dependency visualization, and logical semester planning.

### Table of Contents
- [Features](#features)
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Acknowledgments](#acknowledgments)

---

### Features

The application is built on several key DSA concepts to deliver a powerful user experience:

-   **Graph View:** Courses and their prerequisites are modeled as a directed graph. This view allows users to visualize the entire curriculum's dependencies.
-   **Course Search:** A lightning-fast search bar with auto-completion is powered by a **Trie data structure**.
-   **My Planner:** Based on a user's completed courses, this feature uses **Breadth-First Search (BFS)** to identify all courses they are immediately eligible to take.
-   **Semester Path Planner:** This tool takes a selected semester's courses and arranges them in a logical, prerequisite-first order using **Topological Sort**.

---

### Project Overview

This project consists of a Python-based backend API and a static HTML/CSS/JavaScript frontend.

-   **Frontend:** Built with HTML, CSS (Tailwind CSS via CDN), and vanilla JavaScript.
-   **Backend:** A RESTful API built with Python and the Flask framework, served with `gunicorn`.
-   **Database:** Cloud Firestore, a NoSQL document database provided by Firebase.

### Prerequisites

Before you begin, ensure you have the following installed on your machine:
-   [Python 3.6+](https://www.python.org/)
-   [Git](https://git-scm.com/downloads)
-   [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

---

### Installation and Setup

Follow these steps to get a local copy of the project up and running.

### 1. Clone the Repository


#### Clone the project from your GitHub repository
git clone [https://github.com/your-username/DSA.git](https://github.com/your-username/DSA.git)
cd DSA

### 2. Set up the Python Backend
Create a virtual environment and install the required Python packages.

#### Create a virtual environment
python -m venv venv

#### Activate the virtual environment
##### On macOS/Linux:
source venv/bin/activate
##### On Windows:
venv\Scripts\activate

#### Install dependencies from requirements.txt
pip install -r requirements.txt

### 3. Configure Firebase
The backend needs access to your Firebase Firestore database.

Go to your Firebase project console and create a new project.

Navigate to Firestore Database and start a new database.

Go to Project settings -> Service accounts and click Generate new private key. This will download a JSON file.

Rename the downloaded file to firebase-sa.json and place it in the Backend/ directory.

Warning: This file contains sensitive credentials. It is a best practice to add Backend/firebase-sa.json to your .gitignore file to prevent it from being committed to your public repository.

## 4. Run the Application Locally
Run the Flask development server from the root of your project.


#### Make sure you are in the DSA/ directory and the virtual environment is active
python Backend/app.py
The application will start on http://127.0.0.1:5000. You can now open http://127.0.0.1:5000/index.html in your web browser to use the application.

Usage
Graph View: Click the "Graph View" tab to see a visualization of all courses. Hover over a course node to see its prerequisites and the courses it unlocks.

Course Search: Use the "Course Search" tab to find courses by code or name using the auto-completing search bar.

My Planner: In the "My Planner" tab, check the boxes for courses you have completed. The right panel will automatically update to show you which new courses you are now eligible to take.

Semesters: Select a semester from the dropdown to see the courses for that semester arranged in the correct prerequisite order.

Project Structure
DSA/
├── Backend/
│   ├── app.py              # The main Flask application
│   └── firebase-sa.json    # Firebase service account key (keep private!)
├── Frontend/
│   └── index.html          # The main HTML file with all frontend logic
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── Procfile                # Heroku/Render configuration file
Deployment
This project can be deployed to various hosting platforms that support both a static frontend and a Python backend. We recommend using a platform that integrates directly with your GitHub repository for seamless Continuous Deployment (CD).

Deploy to Render: Render is a great option as it automates deployments from GitHub. You will need to configure environment variables for your Firebase key.

Deploy to Heroku: A classic and reliable PaaS for Python applications. It requires a Procfile and uses heroku CLI commands.

Deploy to Vercel: Vercel is well-known for frontend hosting but also supports Python backends as serverless functions. It requires a specific file structure and a vercel.json file.

Acknowledgments
Flask

Firebase

Tailwind CSS

Gunico
