import sqlite3
import datetime

DB_FILE = "class_data.db"

def init_db():
    """데이터베이스와 테이블을 초기화합니다."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            date TEXT PRIMARY KEY,
            schedule TEXT,
            lunch TEXT,
            todo TEXT,
            supplies TEXT
        )
    ''')
    # 학생 명단 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    # 자리 배치 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS seats (
            position INTEGER PRIMARY KEY,
            student_name TEXT
        )
    ''')
    # 성장 일지 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS growth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            student_name TEXT,
            content TEXT,
            teacher_comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_daily_log(date, schedule, lunch, todo, supplies):
    """일일 기록을 저장하거나 업데이트합니다."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # date는 datetime.date 객체일 수 있으므로 문자열로 변환
    date_str = date.strftime("%Y-%m-%d") if isinstance(date, datetime.date) else str(date)
    
    c.execute('''
        INSERT OR REPLACE INTO daily_logs (date, schedule, lunch, todo, supplies)
        VALUES (?, ?, ?, ?, ?)
    ''', (date_str, schedule, lunch, todo, supplies))
    conn.commit()
    conn.close()

def get_daily_log(date):
    """특정 날짜의 기록을 가져옵니다."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    date_str = date.strftime("%Y-%m-%d") if isinstance(date, datetime.date) else str(date)
    
    c.execute('SELECT schedule, lunch, todo, supplies FROM daily_logs WHERE date = ?', (date_str,))
    result = c.fetchone()
    conn.close()
    return result

# --- 학생 관리 함수 ---
def add_student(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO students (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name FROM students ORDER BY name')
    rows = c.fetchall()
    conn.close()
    return rows

# --- 자리 배치 함수 ---
def save_seat_arrangement(student_names):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM seats') # 기존 배치 삭제
    
    for i, name in enumerate(student_names):
        c.execute('INSERT INTO seats (position, student_name) VALUES (?, ?)', (i, name))
        
    conn.commit()
    conn.close()

def get_seat_arrangement():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT student_name FROM seats ORDER BY position')
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

# --- 성장 일지 함수 ---
def add_growth_log(student_name, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    c.execute('INSERT INTO growth_logs (date, student_name, content) VALUES (?, ?, ?)', 
              (date_str, student_name, content))
    conn.commit()
    conn.close()

def get_student_logs(student_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, date, content, teacher_comment FROM growth_logs WHERE student_name = ? ORDER BY date DESC', (student_name,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_growth_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, date, student_name, content, teacher_comment FROM growth_logs ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def update_teacher_comment(log_id, comment):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE growth_logs SET teacher_comment = ? WHERE id = ?', (comment, log_id))
    conn.commit()
    conn.close()
