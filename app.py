# app.py
from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime, timedelta, date
import re

DB = 'db.sqlite'

app = Flask(__name__)

# --- DB helpers ---
def init_db():
    """Initialize the SQLite database with tasks table"""
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        title TEXT,
        notes TEXT,
        deadline DATE,
        est_minutes INTEGER DEFAULT 60,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        completed INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def query_db(q, args=(), one=False):
    """Execute a query and return results"""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(q, args)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows if not one else (rows[0] if rows else None)

# Initialize database on startup
init_db()

# --- Simple NLP/regex parser ---
SUBJECTS = ['math', 'physics', 'chemistry', 'biology', 'english', 'history', 'computer', 'science']

def parse_nl(text):
    """
    Parse natural language text to extract task details.
    Extracts: subject, title, deadline, and estimated minutes.
    
    Examples:
    - "I have a math exam tomorrow"
    - "Physics homework on 2025-11-22 2 hours"
    - "Chemistry revision today 90 minutes"
    """
    text_low = text.lower()
    
    # Subject detection
    subject = None
    for s in SUBJECTS:
        if re.search(r'\b' + re.escape(s) + r'\b', text_low):
            subject = s.capitalize()
            break
    
    # Date detection: simple words and patterns
    today = date.today()
    deadline = None
    
    if 'tomorrow' in text_low:
        deadline = (today + timedelta(days=1)).isoformat()
    elif 'today' in text_low:
        deadline = today.isoformat()
    elif 'next week' in text_low:
        deadline = (today + timedelta(days=7)).isoformat()
    elif 'next monday' in text_low:
        days_ahead = 0 - today.weekday() + 7  # Next Monday
        if days_ahead <= 0:
            days_ahead += 7
        deadline = (today + timedelta(days=days_ahead)).isoformat()
    else:
        # Find yyyy-mm-dd or dd/mm/yyyy patterns
        m = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        if m:
            deadline = m.group(1)
        else:
            m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', text)
            if m:
                day, month, year = m.groups()
                if len(year) == 2:
                    year = '20' + year
                try:
                    deadline = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    deadline = None
    
    # Duration detection
    est_minutes = 60  # default
    
    # Check for hours
    m = re.search(r'(\d+)\s*(hours|hrs|hr|h)\b', text_low)
    if m:
        est_minutes = int(m.group(1)) * 60
    else:
        # Check for minutes
        m = re.search(r'(\d+)\s*(minutes|mins|min|m)\b', text_low)
        if m:
            est_minutes = int(m.group(1))
    
    # Title fallback - use the original text
    title = text if len(text) < 120 else text[:120]
    
    return {
        'subject': subject or 'General',
        'title': title,
        'deadline': deadline,
        'est_minutes': est_minutes
    }

# --- Routes ---
@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks from database"""
    rows = query_db('SELECT id, subject, title, notes, deadline, est_minutes, completed FROM tasks ORDER BY deadline')
    tasks = [dict(zip(['id','subject','title','notes','deadline','est_minutes','completed'], tuple(r))) for r in rows]
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task from form data"""
    data = request.get_json() or request.form
    subject = data.get('subject') or 'General'
    title = data.get('title') or 'Untitled'
    notes = data.get('notes') or ''
    deadline = data.get('deadline') or None
    est = int(data.get('est_minutes') or 60)
    
    query_db('INSERT INTO tasks (subject,title,notes,deadline,est_minutes) VALUES (?,?,?,?,?)',
             (subject, title, notes, deadline, est))
    return jsonify({'status':'ok', 'message': 'Task created successfully'})

@app.route('/api/tasks/nl', methods=['POST'])
def create_task_nl():
    """Create a task from natural language input"""
    data = request.get_json()
    text = data.get('text','')
    
    if not text:
        return jsonify({'status':'error', 'message': 'No text provided'}), 400
    
    parsed = parse_nl(text)
    query_db('INSERT INTO tasks (subject,title,deadline,est_minutes) VALUES (?,?,?,?)',
             (parsed['subject'], parsed['title'], parsed['deadline'], parsed['est_minutes']))
    
    return jsonify({'status':'ok', 'parsed':parsed, 'message': 'Task created from natural language'})

@app.route('/api/generate', methods=['POST'])
def generate_plan():
    """
    Generate today's study plan based on available time and pending tasks.
    Algorithm: Sort tasks by deadline, allocate time from earliest deadline first.
    """
    data = request.get_json() or {}
    minutes = int(data.get('available_minutes', 180))
    today_str = data.get('date') or date.today().isoformat()
    
    # Load pending tasks ordered by deadline (earliest first)
    rows = query_db('SELECT id,subject,title,deadline,est_minutes FROM tasks WHERE completed=0 ORDER BY deadline')
    tasks = [dict(zip(['id','subject','title','deadline','est_minutes'], tuple(r))) for r in rows]
    
    # Simple planning algorithm
    plan = []
    remaining = minutes
    
    for t in tasks:
        if remaining <= 0:
            break
        
        # Allocate time to this task (up to its estimated duration)
        take = min(remaining, t['est_minutes'])
        plan.append({
            'task_id': t['id'],
            'subject': t['subject'],
            'title': t['title'],
            'deadline': t['deadline'],
            'minutes': take
        })
        remaining -= take
    
    return jsonify({
        'date': today_str,
        'available_minutes': minutes,
        'used_minutes': minutes - remaining,
        'remaining_minutes': remaining,
        'plan': plan
    })

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    query_db('UPDATE tasks SET completed=1 WHERE id=?', (task_id,))
    return jsonify({'status':'ok', 'message': 'Task marked as completed'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    query_db('DELETE FROM tasks WHERE id=?', (task_id,))
    return jsonify({'status':'ok', 'message': 'Task deleted'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about tasks"""
    total = query_db('SELECT COUNT(*) as count FROM tasks', one=True)
    completed = query_db('SELECT COUNT(*) as count FROM tasks WHERE completed=1', one=True)
    pending = query_db('SELECT COUNT(*) as count FROM tasks WHERE completed=0', one=True)
    
    return jsonify({
        'total': total[0] if total else 0,
        'completed': completed[0] if completed else 0,
        'pending': pending[0] if pending else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
