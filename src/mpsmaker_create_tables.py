import psycopg2
from psycopg2 import sql
import random

# Connection parameters
db_params = {
    "host": "dpg-cs2tbi3v2p9s738oaq7g-a.oregon-postgres.render.com",
    "database": "mpsmaker_postgresql",
    "user": "mpsmaker_postgresql_user",
    "password": "Mf1UXlve7Q5R6HN3aO6d2elEErzXpz7b",
    "port": "5432"
}

# Connect to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create usuarios table
cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255),
        email VARCHAR(255),
        senha VARCHAR(255),
        ativo BOOLEAN
    )
""")

# Create livros table
cur.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR(255),
        qtde_paginas INTEGER,
        dono INTEGER REFERENCES usuarios(id)
    )
""")

# Commit the changes
conn.commit()

print("Tables 'usuarios' and 'livros' have been created successfully.")


# Function to insert fictional users
def insert_fictional_users(cur, num_users=10):
    for i in range(num_users):
        nome = f"User {i+1}"
        email = f"user{i+1}@example.com"
        senha = f"password{i+1}"
        ativo = random.choice([True, False])
        
        cur.execute("""
            INSERT INTO usuarios (nome, email, senha, ativo)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, senha, ativo))
    
    print(f"{num_users} fictional users have been inserted.")

# Function to insert fictional books
def insert_fictional_books(cur, num_books=20):
    cur.execute("SELECT id FROM usuarios")
    user_ids = [row[0] for row in cur.fetchall()]
    
    for i in range(num_books):
        titulo = f"Book {i+1}"
        qtde_paginas = random.randint(50, 500)
        dono = random.choice(user_ids)
        
        cur.execute("""
            INSERT INTO livros (titulo, qtde_paginas, dono)
            VALUES (%s, %s, %s)
        """, (titulo, qtde_paginas, dono))
    
    print(f"{num_books} fictional books have been inserted.")

# Function to view users data
def view_users(cur):
    cur.execute("SELECT * FROM usuarios")
    users = cur.fetchall()
    print("\nUsers:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Active: {user[4]}")

# Function to view books data
def view_books(cur):
    cur.execute("""
        SELECT l.id, l.titulo, l.qtde_paginas, u.nome as dono
        FROM livros l
        JOIN usuarios u ON l.dono = u.id
    """)
    books = cur.fetchall()
    print("\nBooks:")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Pages: {book[2]}, Owner: {book[3]}")

# After creating tables, insert fictional data
# insert_fictional_users(cur)
# insert_fictional_books(cur)

# View the inserted data
view_users(cur)
view_books(cur)

# Commit the changes
conn.commit()

print("Fictional data has been inserted successfully.")


# Close the cursor and connection
cur.close()
conn.close()