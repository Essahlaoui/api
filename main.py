from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from typing import List

# Création de la base de données
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Création de la table des étudiants
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        grade INTEGER NOT NULL
    )
''')

# Fermeture de la connexion
conn.close()

# Création de l'application FastAPI
app = FastAPI()

# Définition du modèle de données pour un étudiant
class Student(BaseModel):
    id: int
    name: str
    grade: int

# Liste des étudiants
@app.get("/students/", response_model=List[Student])
def read_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

# Création d'un nouvel étudiant
@app.post("/students/", response_model=Student)
def create_student(student: Student):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (student.name, student.grade))
    conn.commit()
    conn.close()
    return student

# Mise à jour d'un étudiant
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (student.name, student.grade, student_id))
    conn.commit()
    conn.close()
    return student

# Suppression d'un étudiant
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"message": "Étudiant supprimé"}
