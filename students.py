import sqlite3
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI(title="student management")

def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
cursor = conn.cursor()

cursor.execute("""
create table if not exists students (
    id integer primary key autoincrement,
    name text not null,
    age interger not null,
    course text not null
    )
""")

conn.commit()
conn.close()

class Student(BaseModel):
    name : str
    age: int
    course: str

class UpdateStudent(BaseModel):
    name: str | None = None
    age: int | None = None
    course: str | None=None

@app.post("/students")
def add(student:Student):
    conn=get_db()
    cursor = conn.cursor()
    cursor.execute("insert into students (name,age,course) values (?,?,?)",
                   (student.name,student.age,student.course))
    conn.commit()
    student_id=cursor.lastrowid
    conn.close()
    return {"message": "Student added successfully!", "id": student_id}

@app.get("/students")
def view():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("select * from students")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/students/search")
def search(key:str):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("select * from students where name like ? or course like ?",
                   (f"%{key}",f"%{key}"))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="No matching results found")
    return [dict(row) for row in rows]

@app.put("/students/{student_id}")
def update(student_id : int,student : UpdateStudent):
    conn = get_db()
    cursor = conn.cursor()
    
    # Only update provided fields
    update_fields = []
    params = []
    if student.name:
        update_fields.append("name=?")
        params.append(student.name)
    if student.age:
        update_fields.append("age=?")
        params.append(student.age)
    if student.course:
        update_fields.append("course=?")
        params.append(student.course)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    params.append(student_id)
    query = f"UPDATE students SET {', '.join(update_fields)} WHERE id=?"
    cursor.execute(query, tuple(params))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    conn.close()
    return {"message": "Student updated successfully"}

@app.delete("/students/{student_id}")
def delete(student_id: int):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("delete from students where id=?",(student_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    conn.close()
    return {"message": "Student deleted successfully"}
