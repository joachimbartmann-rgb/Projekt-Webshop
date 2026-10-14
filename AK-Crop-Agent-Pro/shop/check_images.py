import sqlite3
from pathlib import Path

db_file = (
    Path(__file__).parent.parent /
    "Database" /
    "collection_v2.db"
)

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM images
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()