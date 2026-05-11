import os
import mysql.connector
from mysql.connector import Error

# Záložné dáta (keď DB nie je dostupná)
STUDENTS_FALLBACK = [
    {"id": 1, "name": "Adrian",  "surname": "Červenka",  "nickname": "chilli pepper", "image": "https://picsum.photos/id/1011/300/200",       "bio": "Má fakt divné hlášky."},
    {"id": 2, "name": "Milan",   "surname": "Kokina",    "nickname": "tanečník",       "image": "https://api.sportnet.online/v1/ppo/futbalsfz.sk/users/5efee63f1b04f230d150c5ce/formal-photo/e18f5e4d-9a8d-4196-9e18-30ebf1b60dc4", "bio": "Nechcelo sa mi toto vobec robiť."},
    {"id": 3, "name": "Martin",  "surname": "Jelínek",   "nickname": "král jelimán",   "image": "https://api.sportnet.online/v1/ppo/futbalsfz.sk/users/68c9112594d10f7e9dd591c4/formal-photo/94387b0f-c431-49e2-b562-6a357f415c2d", "bio": "............"},
    {"id": 4, "name": "Daniel",  "surname": "Barta",     "nickname": "skeleton",       "image": "https://picsum.photos/id/1014/300/200",       "bio": "..........."},
    {"id": 5, "name": "Matej",   "surname": "Randziak",  "nickname": "tankista",       "image": "https://picsum.photos/id/1015/300/200",       "bio": "..........."},
    {"id": 6, "name": "Matúš",   "surname": "Bucko",     "nickname": "xxxxxxxx",       "image": "https://picsum.photos/id/1016/300/200",       "bio": "Nechcelo sa mi toto vobec robiť."},
    {"id": 7, "name": "Janka",   "surname": "Vargová",   "nickname": "xxxxxxxxx",      "image": "https://picsum.photos/id/1018/300/200",       "bio": "Má fakt divné hlášky."},
    {"id": 8, "name": "Matúš",   "surname": "Holečka",   "nickname": "xxxxxxxxxx",     "image": "https://picsum.photos/id/1019/300/200",       "bio": "............"},
    {"id": 9, "name": "Marko",   "surname": "Mihalička", "nickname": "xxxxxxxxxx",     "image": "https://picsum.photos/id/1020/300/200",       "bio": "............"},
    {"id": 10,"name": "Lukáš",   "surname": "Vindiš",    "nickname": "žirafa",         "image": "https://picsum.photos/id/1021/300/200",       "bio": "............"},
]

_connection = None


def get_connection():
    """Vráti aktívne DB spojenie alebo None, ak nie je dostupné."""
    global _connection
    try:
        if _connection and _connection.is_connected():
            return _connection
        _connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "school_db"),
        )
        print("✅ Pripojené k MariaDB")
        return _connection
    except Error as e:
        print(f"⚠️  DB nedostupná (bežím v režime bez DB): {e}")
        return None


def get_students():
    """Načíta študentov z DB; ak sa to nepodarí, vráti záložné dáta."""
    conn = get_connection()
    if conn is None:
        return STUDENTS_FALLBACK

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        return rows if rows else STUDENTS_FALLBACK
    except Error as e:
        print(f"⚠️  Chyba dopytu, používam záložné dáta: {e}")
        return STUDENTS_FALLBACK
