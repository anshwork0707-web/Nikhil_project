"""
Populate the database with sample tasks for demonstration
Run this script to add realistic sample data to your Study Planner
"""

import sqlite3
from datetime import datetime, timedelta
import random

DB = 'db.sqlite'

# Sample tasks organized by subject
SAMPLE_TASKS = {
    'Math': [
        'Calculus Chapter 5: Derivatives and Applications',
        'Linear Algebra: Matrix Operations Practice',
        'Solve 20 problems from Trigonometry workbook',
        'Prepare for Midterm: Integration Techniques',
        'Complete homework on Differential Equations',
        'Study probability and statistics concepts',
        'Practice geometry proofs',
        'Review algebraic expressions and equations',
        'Complete assignment on Number Theory',
        'Prepare presentation on Mathematical Modeling'
    ],
    'Physics': [
        'Mechanics Chapter 3: Newton\'s Laws of Motion',
        'Lab report on Pendulum Experiment',
        'Thermodynamics problem set completion',
        'Study Electromagnetic Waves theory',
        'Optics practical exam preparation',
        'Complete quantum mechanics assignment',
        'Review kinematics formulas',
        'Prepare for viva on Electricity and Magnetism',
        'Modern Physics reading: Relativity',
        'Complete lab notebook for Wave Motion'
    ],
    'Chemistry': [
        'Organic Chemistry: Reaction Mechanisms study',
        'Lab report: Titration Experiment',
        'Periodic Table trends and properties review',
        'Chemical Bonding chapter notes',
        'Prepare for practical exam: Qualitative Analysis',
        'Complete stoichiometry problem set',
        'Study Electrochemistry concepts',
        'Polymer Chemistry assignment',
        'Review Thermochemistry calculations',
        'Inorganic Chemistry coordination compounds'
    ],
    'Biology': [
        'Cell Biology: Mitosis and Meiosis diagrams',
        'Genetics problem solving: Punnett squares',
        'Ecology project: Local ecosystem study',
        'Human Anatomy chapter reading',
        'Plant Physiology lab report',
        'Evolution and Natural Selection essay',
        'Microbiology culture experiment',
        'Molecular Biology: DNA Replication notes',
        'Prepare for dissection practical',
        'Biotechnology case study presentation'
    ],
    'English': [
        'Essay: Analysis of Shakespeare\'s Macbeth',
        'Grammar exercises: Active and Passive Voice',
        'Novel reading: 1984 by George Orwell',
        'Poetry analysis: Romantic Era poets',
        'Vocabulary building: 50 new words',
        'Creative writing assignment: Short story',
        'Literary criticism presentation',
        'Research paper on Modern Literature',
        'Rhetoric and Composition practice',
        'Prepare for oral presentation on Hamlet'
    ],
    'History': [
        'World War II: Causes and Consequences essay',
        'Ancient Civilizations comparison project',
        'Industrial Revolution timeline creation',
        'Read chapters on American Civil War',
        'Medieval History document analysis',
        'Cold War presentation preparation',
        'Renaissance Art and Culture study',
        'Constitutional History assignment',
        'Prepare for quiz on French Revolution',
        'Modern Indian History case study'
    ],
    'Computer': [
        'Python programming: Data Structures assignment',
        'Database Management: SQL queries practice',
        'Web Development: Complete Portfolio Website',
        'Algorithm Analysis: Sorting algorithms study',
        'Operating Systems: Process Scheduling lab',
        'Computer Networks: TCP/IP protocol study',
        'Machine Learning project: Linear Regression',
        'Software Engineering: UML diagrams',
        'Cybersecurity assignment on Encryption',
        'Prepare presentation on Cloud Computing'
    ],
    'General': [
        'Library book return and renewal',
        'Submit scholarship application form',
        'Attend student council meeting',
        'Register for next semester courses',
        'Meet with academic advisor',
        'Complete internship application',
        'Prepare resume for job fair',
        'Attend workshop on Time Management',
        'Submit hostel fee payment',
        'Update personal portfolio website'
    ]
}

def clear_database():
    """Clear existing tasks (optional)"""
    conn = sqlite3.connect(DB)
    conn.execute('DELETE FROM tasks')
    conn.commit()
    conn.close()
    print("✓ Cleared existing tasks")

def populate_tasks(num_tasks=50, clear_first=False):
    """
    Populate database with sample tasks
    
    Args:
        num_tasks: Number of tasks to create (default: 50)
        clear_first: Whether to clear existing tasks first (default: False)
    """
    
    if clear_first:
        clear_database()
    
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    today = datetime.now().date()
    tasks_added = 0
    
    # Distribute tasks across subjects
    subjects = list(SAMPLE_TASKS.keys())
    
    for i in range(num_tasks):
        # Cycle through subjects
        subject = subjects[i % len(subjects)]
        
        # Pick a random task from that subject
        task_pool = SAMPLE_TASKS[subject]
        title = random.choice(task_pool)
        
        # Generate random deadline (between today and 30 days from now)
        days_ahead = random.randint(0, 30)
        deadline = (today + timedelta(days=days_ahead)).isoformat()
        
        # Random estimated time (30, 45, 60, 90, 120, 150, 180 minutes)
        est_minutes = random.choice([30, 45, 60, 90, 120, 150, 180])
        
        # Some tasks are already completed (20% chance)
        completed = 1 if random.random() < 0.2 else 0
        
        # Insert task
        cursor.execute('''
            INSERT INTO tasks (subject, title, deadline, est_minutes, completed)
            VALUES (?, ?, ?, ?, ?)
        ''', (subject, title, deadline, est_minutes, completed))
        
        tasks_added += 1
        
        # Print progress every 10 tasks
        if tasks_added % 10 == 0:
            print(f"Added {tasks_added} tasks...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Successfully added {tasks_added} sample tasks!")
    print(f"✓ Database: {DB}")
    print(f"✓ Date range: Today to {(today + timedelta(days=30)).isoformat()}")
    
    # Show summary
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    total = cursor.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    pending = cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed=0').fetchone()[0]
    completed_count = cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed=1').fetchone()[0]
    
    print(f"\n📊 Database Summary:")
    print(f"   Total Tasks: {total}")
    print(f"   Pending: {pending}")
    print(f"   Completed: {completed_count}")
    
    # Show tasks by subject
    print(f"\n📚 Tasks by Subject:")
    subject_counts = cursor.execute('''
        SELECT subject, COUNT(*) as count 
        FROM tasks 
        GROUP BY subject 
        ORDER BY count DESC
    ''').fetchall()
    
    for subject, count in subject_counts:
        print(f"   {subject}: {count} tasks")
    
    conn.close()

def add_urgent_tasks():
    """Add some urgent tasks due today or tomorrow for testing"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    urgent_tasks = [
        ('Math', 'URGENT: Submit Calculus Assignment', today.isoformat(), 120),
        ('Physics', 'Prepare for Tomorrow\'s Lab Exam', tomorrow.isoformat(), 90),
        ('Chemistry', 'Complete Organic Chemistry Quiz', today.isoformat(), 60),
        ('English', 'Finish Essay Draft - Due Tomorrow', tomorrow.isoformat(), 150),
        ('Computer', 'Debug Python Project - Submission Today', today.isoformat(), 180)
    ]
    
    for subject, title, deadline, est_minutes in urgent_tasks:
        cursor.execute('''
            INSERT INTO tasks (subject, title, deadline, est_minutes, completed)
            VALUES (?, ?, ?, ?, 0)
        ''', (subject, title, deadline, est_minutes))
    
    conn.commit()
    conn.close()
    
    print(f"\n⚠️ Added {len(urgent_tasks)} urgent tasks for immediate scheduling!")

if __name__ == '__main__':
    print("=" * 60)
    print("   STUDY PLANNER - DATABASE POPULATION SCRIPT")
    print("=" * 60)
    print()
    
    # Ask user preferences
    print("Options:")
    print("1. Add 50 sample tasks (keep existing)")
    print("2. Add 100 sample tasks (keep existing)")
    print("3. Clear database and add 50 tasks")
    print("4. Clear database and add 100 tasks")
    print("5. Add only urgent tasks (5 tasks)")
    print()
    
    choice = input("Enter your choice (1-5) [default: 1]: ").strip() or "1"
    
    print()
    
    if choice == "1":
        populate_tasks(50, clear_first=False)
    elif choice == "2":
        populate_tasks(100, clear_first=False)
    elif choice == "3":
        populate_tasks(50, clear_first=True)
    elif choice == "4":
        populate_tasks(100, clear_first=True)
    elif choice == "5":
        add_urgent_tasks()
    else:
        print("Invalid choice! Running default (50 tasks)...")
        populate_tasks(50, clear_first=False)
    
    print()
    print("=" * 60)
    print("✓ DONE! Refresh your browser to see the new tasks.")
    print("=" * 60)
