from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

users = [r[0] for r in db.execute(text(
    "select column_name from information_schema.columns "
    "where table_schema='public' and table_name='users' "
    "order by ordinal_position"
)).fetchall()]

students = [r[0] for r in db.execute(text(
    "select column_name from information_schema.columns "
    "where table_schema='public' and table_name='students' "
    "order by ordinal_position"
)).fetchall()]

print("users cols =", users)
print("students cols =", students)

db.close()
