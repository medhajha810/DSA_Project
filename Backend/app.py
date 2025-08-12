# main.py
# This Flask application provides a RESTful API for the University Course Recommender System.
# It uses an in-memory Graph and Trie data structure, populated from a Firestore database.
#
# To run this, you will need to:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Set up a Firebase project and download your service account key (as `firebase-sa.json`).
# 3. Run the app: python main.py

import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

# --- Data Structures and Algorithms ---

class CourseGraph:
    """Represents the course dependencies as a directed graph."""
    def __init__(self):
        self.adjList = {}
        self.nodes = {}

    def add_node(self, course_id, course_data):
        """Adds a course node to the graph."""
        if course_id not in self.adjList:
            self.adjList[course_id] = []
            self.nodes[course_id] = course_data

    def add_edge(self, prereq_id, course_id):
        """Adds a directed edge from a prerequisite to a course."""
        if prereq_id in self.adjList and course_id in self.adjList:
            self.adjList[prereq_id].append(course_id)

    def get_neighbors(self, course_id):
        """Returns the list of courses that have the given course as a prerequisite."""
        return self.adjList.get(course_id, [])

    def get_node(self, course_id):
        """Returns the data for a specific course node."""
        return self.nodes.get(course_id)

    def get_all_nodes(self):
        """Returns all course nodes."""
        return list(self.nodes.values())

    def bfs_recommendations(self, completed_courses):
        """
        Uses Breadth-First Search (BFS) to find courses a student is eligible to take.
        """
        completed_set = set(completed_courses)
        recommendations = set()

        for course_id, course_data in self.nodes.items():
            if course_id not in completed_set:
                prereqs = course_data.get('prerequisites', [])
                if all(p in completed_set for p in prereqs):
                    recommendations.add(course_id)
        
        return list(recommendations)

    def topological_sort(self, course_ids):
        """
        Performs a topological sort on a subset of the graph to find a valid course path.
        """
        in_degree = {c_id: 0 for c_id in course_ids}
        adj_list_subset = {c_id: [] for c_id in course_ids}
        
        for prereq_id in course_ids:
            for course_id in self.adjList.get(prereq_id, []):
                if course_id in course_ids:
                    adj_list_subset[prereq_id].append(course_id)
                    in_degree[course_id] += 1
        
        queue = [c_id for c_id in course_ids if in_degree[c_id] == 0]
        sorted_list = []
        
        while queue:
            node = queue.pop(0)
            sorted_list.append(node)
            for neighbor in adj_list_subset.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(sorted_list) != len(course_ids):
             return {"error": "Graph contains a cycle and cannot be sorted topologically."}

        path = []
        completed_in_path = set()
        remaining = set(sorted_list)

        while remaining:
            semester = []
            available_this_semester = list(remaining)
            for course_id in available_this_semester:
                prereqs = self.get_node(course_id).get('prerequisites', [])
                if all(p in completed_in_path for p in prereqs):
                    semester.append(course_id)
            
            if not semester:
                break 

            path.append(semester)
            for c in semester:
                completed_in_path.add(c)
                remaining.remove(c)
        
        return path

class TrieNode:
    """A node in the Trie data structure."""
    def __init__(self):
        self.children = {}
        self.course_ids = []

class Trie:
    """
    Implements a Trie (Prefix Tree) for efficient course searching.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, course_id):
        """Inserts a word into the trie."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.course_ids.append(course_id)

    def search(self, prefix):
        """Finds all course IDs that start with the given prefix."""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        results = self._find_all_ids(node)
        return list(set(results))

    def _find_all_ids(self, node):
        """Helper function to find all IDs from a given node downwards."""
        results = []
        results.extend(node.course_ids)
        for child_node in node.children.values():
            results.extend(self._find_all_ids(child_node))
        return results

# --- Flask App Configuration and Initialization ---

app = Flask(__name__)
CORS(app)

# Firebase initialization
try:
    cred = credentials.Certificate('firebase-sa.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    db = None

course_graph = CourseGraph()
course_trie = Trie()
semesters = {}

def load_data():
    """Loads all course and semester data from Firestore into memory."""
    print("Loading data from Firestore...")
    global course_graph, course_trie, semesters
    course_graph = CourseGraph()
    course_trie = Trie()
    semesters = {}
    
    courses_ref = db.collection('courses').stream()
    course_data_list = []
    for doc in courses_ref:
        data = doc.to_dict()
        data['id'] = doc.id
        course_data_list.append(data)

    for data in course_data_list:
        course_graph.add_node(data['id'], data)
        course_trie.insert(data['id'], data['id'])
        course_trie.insert(data['Name'], data['id'])
    
    for data in course_data_list:
        prereqs = data.get('prerequisites', [])
        for prereq_id in prereqs:
            course_graph.add_edge(prereq_id, data['id'])

    semesters_ref = db.collection('semesters').stream()
    for doc in semesters_ref:
        semesters[doc.id] = doc.to_dict()
    
    print("Data loading complete.")

if db:
    load_data()

# --- API Endpoints ---

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Endpoint to get all courses."""
    return jsonify(course_graph.get_all_nodes())

@app.route('/api/semesters', methods=['GET'])
def get_semesters():
    """Endpoint to get all semesters."""
    return jsonify(semesters)

@app.route('/api/semesters/<semester_id>', methods=['GET'])
def get_semester_courses(semester_id):
    """Endpoint to get courses for a specific semester."""
    semester = semesters.get(semester_id)
    if not semester:
        return jsonify({"error": "Semester not found"}), 404
    return jsonify(semester.get('courses', []))

@app.route('/api/courses/search', methods=['GET'])
def search_courses():
    """Endpoint to search for courses using a trie."""
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    
    course_ids = course_trie.search(query)
    results = [course_graph.get_node(c_id) for c_id in course_ids]
    return jsonify(results)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Endpoint to get course recommendations based on completed courses.
    Request body: {"completed_courses": ["CS101", "MA101"]}
    """
    data = request.json
    completed_courses = data.get('completed_courses', [])
    if not isinstance(completed_courses, list):
        return jsonify({"error": "completed_courses must be a list"}), 400
    
    recommendations = course_graph.bfs_recommendations(completed_courses)
    return jsonify(recommendations)

@app.route('/api/course/<course_id>', methods=['GET'])
def get_course_details(course_id):
    """Endpoint to get details for a specific course."""
    course_details = course_graph.get_node(course_id)
    if not course_details:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
