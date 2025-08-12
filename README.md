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

#### 1. Clone the Repository

```bash
# Clone the project from your GitHub repository
git clone [https://github.com/your-username/DSA.git](https://github.com/your-username/DSA.git)
cd DSA
