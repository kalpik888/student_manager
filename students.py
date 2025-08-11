import sqlite3

conn = sqlite3.connect("students.db")
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


def add():
    name= input("enter name: ")
    age= input("enter age: ")
    course= input("enter course: ")
    cursor.execute("insert into students (name,age,course) values (?,?,?)",
                   (name,age,course))
    conn.commit()
    print("students added successfully!!!")


def view():
    cursor.execute("select * from students")
    rows = cursor.fetchall()
    print("\n---Student Records---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Course: {row[3]}")
    if not rows:
        print("no records found")

def search():
    key= input("enter the keyword to search: ")
    cursor.execute("select * from students where name like ? or course like ?",
                   (f"%{key}",f"%{key}"))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Course: {row[3]}")
    else:
        print("no matching results found")

def update():
    student_id= input("enter student id: ")
    name = input("enter the new name: ")
    age= input("enter the new age: ")
    course = input("enter the new course: ")
    cursor.execute("update students set name=?,age=?,course=? where id=?",
                   (name,age,course,student_id))
    conn.commit()
    if cursor.rowcount >0:
        print("student data updated!!!")
    else:
        print("student not found")

def delete():
    student_id=input("enter id to delete: ")
    cursor.execute("delete from students where id=?",(student_id))
    conn.commit()
    if cursor.rowcount >0:
        print("student deleted")
    else:
        print("student not found")


while True:
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add()
    elif choice == "2":
        view()
    elif choice == "3":
        search()
    elif choice == "4":
        update()
    elif choice == "5":
        delete()
    elif choice == "6":
        print("Exiting... Goodbye!")
        break
    else:
        print("❌ Invalid choice, please try again.")

# Close the database connection
conn.close()
