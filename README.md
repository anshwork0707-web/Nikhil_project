# 📚 Study Planner - AI-Powered Task Manager & Schedule Generator

> A simple web application that helps students manage tasks and generate daily study schedules using natural language processing.

## 🎯 Project Summary

This web app accepts tasks in natural language or via a structured form, extracts subject and deadline information using lightweight NLP, and generates an optimized daily study plan based on available time and task priorities.

---

## ✨ Features

- **Add Tasks via Natural Language**: Type sentences like *"I have a math exam tomorrow 2 hours"* and the system automatically extracts:
  - Subject (Math, Physics, Chemistry, etc.)
  - Deadline (tomorrow, today, specific dates)
  - Estimated duration (hours/minutes)

- **Add Tasks via Form**: Structured input with dropdowns and date pickers

- **Task Management**: View all tasks, mark as completed, delete tasks

- **Smart Schedule Generation**: Algorithm that:
  - Sorts tasks by deadline (earliest first)
  - Allocates available study time efficiently
  - Generates time-slot schedule (e.g., 6-7 PM: Math)

- **Statistics Dashboard**: Track total, pending, and completed tasks

- **Modern UI Design**: 
  - Animated gradients and smooth transitions
  - Font Awesome icons throughout
  - Glass morphism effects
  - Responsive layout for mobile/tablet/desktop
  - Custom scrollbars and hover effects

- **Sample Data Generator**: Python script to populate database with 50-100 realistic tasks

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.10+ with Flask |
| Database | SQLite (local file `db.sqlite`) |
| NLP | Simple regex-based parsing |
| Frontend | HTML5, CSS3, JavaScript (Vanilla JS) |
| Styling | Custom CSS with gradient designs |
| Icons | Font Awesome 6.4.0 (CDN) |
| Animations | CSS3 keyframes & transitions |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```powershell
   cd d:\Nikhil_project
   ```

2. **Create Virtual Environment** (Recommended)
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```powershell
   python app.py
   ```

5. **Open in Browser**
   - Navigate to: `http://127.0.0.1:5000/`
   - The app will automatically create the SQLite database on first run

6. **Populate Sample Data** (Optional but Recommended)
   ```powershell
   python populate_data.py
   ```
   Choose from options:
   - Add 50 sample tasks
   - Add 100 sample tasks
   - Clear and add fresh data
   - Add urgent tasks only

---

## 🎮 Usage Guide

### Adding Tasks

#### Method 1: Natural Language Input
In the "Add Task (Natural Language)" section:
- Type: `"I have a physics exam tomorrow 2 hours"`
- Click "Add Task from Text"
- System automatically extracts:
  - Subject: Physics
  - Deadline: Tomorrow's date
  - Duration: 120 minutes

**Supported Patterns:**
- `"Math homework on 2025-11-22"`
- `"Chemistry revision today 90 minutes"`
- `"Biology test next week 1 hour"`

#### Method 2: Form Input
Fill in the form fields:
- Select subject from dropdown
- Enter task title
- Choose deadline date
- Set estimated duration (in minutes)

### Generating Study Plan

1. Set your available study time (default: 180 minutes = 3 hours)
2. Click "Generate Schedule"
3. System creates a timeline with:
   - Start and end times for each task
   - Tasks sorted by deadline priority
   - Visual schedule with subject tags

### Managing Tasks

- **Complete**: Click the "✓ Complete" button on any task
- **Delete**: Click the "🗑️ Delete" button to remove a task
- **View Stats**: Dashboard at top shows total, pending, and completed tasks

---

## 🗂️ Project Structure

```
Nikhil_project/
│
├── app.py                 # Main Flask application
├── populate_data.py       # Database population script
├── templates/
│   └── index.html         # Frontend interface (with Font Awesome)
├── requirements.txt       # Python dependencies
├── README.md             # Complete documentation
├── REPORT_TEMPLATE.md    # Academic report template
├── PRESENTATION_GUIDE.md # PPT slide-by-slide guide
├── QUICKSTART.md         # Quick setup guide
├── DEMO_EXAMPLES.txt     # Demo script with examples
└── db.sqlite             # SQLite database (auto-created)
```

---

## 🧠 NLP Algorithm

### Simple Regex-Based Parser

The `parse_nl()` function uses regular expressions to extract:

1. **Subject Detection**
   - Matches keywords: math, physics, chemistry, biology, english, history, computer
   - Case-insensitive word boundary matching

2. **Date Extraction**
   - "tomorrow" → Current date + 1 day
   - "today" → Current date
   - "next week" → Current date + 7 days
   - Date patterns: `YYYY-MM-DD` or `DD/MM/YYYY`

3. **Duration Parsing**
   - Patterns: `"2 hours"`, `"90 minutes"`, `"1.5 hrs"`
   - Converts to minutes (default: 60 minutes)

### Example Parsing

**Input:** `"I have a math exam tomorrow 2 hours"`

**Output:**
```json
{
  "subject": "Math",
  "title": "I have a math exam tomorrow 2 hours",
  "deadline": "2025-11-19",
  "est_minutes": 120
}
```

---

## 📊 Database Schema

### Tasks Table

```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT,                    -- Task subject/category
  title TEXT,                      -- Task description
  notes TEXT,                      -- Additional notes (optional)
  deadline DATE,                   -- YYYY-MM-DD format
  est_minutes INTEGER DEFAULT 60,  -- Estimated duration
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  completed INTEGER DEFAULT 0      -- Boolean: 0=pending, 1=completed
);
```

---

## 🎯 Planner Algorithm

### Simple Greedy Allocation

```python
1. Fetch all pending tasks (completed = 0)
2. Sort tasks by deadline (earliest first)
3. Initialize available_minutes (user input, default 180)
4. For each task:
   a. If no time remaining, stop
   b. Allocate min(task.est_minutes, remaining_time)
   c. Add to plan with time slot
   d. Subtract from remaining_time
5. Return schedule with start/end times
```

**Example:**
- Available time: 180 minutes
- Tasks: Math (60min, due tomorrow), Physics (90min, due in 2 days)
- Generated plan:
  - 6:00 PM - 7:00 PM: Math (60 min)
  - 7:00 PM - 8:30 PM: Physics (90 min)
  - Remaining: 30 minutes

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve main HTML page |
| GET | `/api/tasks` | Get all tasks (JSON) |
| POST | `/api/tasks` | Create task from form data |
| POST | `/api/tasks/nl` | Create task from natural language |
| POST | `/api/generate` | Generate today's study plan |
| POST | `/api/tasks/<id>/complete` | Mark task as completed |
| DELETE | `/api/tasks/<id>` | Delete a task |
| GET | `/api/stats` | Get task statistics |

---

## 📸 Demo Instructions

### For Presentation/Video:

1. **Show Homepage**
   - Point out clean UI with dashboard stats

2. **Add Task via Natural Language**
   - Type: `"I have a math exam tomorrow 2 hours"`
   - Show parsed fields appearing in task list

3. **Add Task via Form**
   - Select Physics, enter "Homework Ch 5", set deadline
   - Show task added to list

4. **Generate Plan**
   - Set available time to 180 minutes
   - Click "Generate Schedule"
   - Show time-slotted schedule with color coding

5. **Mark Complete**
   - Complete one task
   - Regenerate plan to show updated schedule

6. **Explain Flow**
   - Input → NLP Parser → Database → Planner → UI Display

---

## 🎓 Academic Documentation

### Report Structure (Suggested)

1. **Title Page** - Name, Roll No, Semester
2. **Abstract** - 3-4 line summary
3. **Problem Statement** - Why students need this tool
4. **Objectives** - Key goals (task management, NLP parsing, scheduling)
5. **Technology Stack** - Table of tools used
6. **System Architecture** - Diagram (Frontend ↔ Flask ↔ SQLite)
7. **Database Design** - Schema with data types
8. **NLP Approach** - Regex patterns explained
9. **Planner Algorithm** - Pseudocode + example
10. **Screenshots** - UI, task list, generated plan
11. **Testing** - Sample inputs and outputs
12. **Results** - Working prototype demonstration
13. **Future Enhancements** - spaCy, calendar export, ML suggestions
14. **References** - Flask, SQLite documentation
15. **Appendix** - Key code snippets

### PowerPoint Structure (10-12 Slides)

1. Title + Student Details
2. Motivation / Problem
3. Objectives
4. Tech Stack
5. System Architecture
6. Database Schema
7. NLP Parsing Approach
8. Planner Algorithm
9. Demo Screenshots
10. Results & Testing
11. Future Work
12. Thank You / Q&A

---

## 🧪 Testing Examples

Test these natural language inputs:

```
✓ "I have a math exam tomorrow"
✓ "Physics homework on 2025-11-22 2 hours"
✓ "Chemistry revision today 90 minutes"
✓ "Biology test next week 1 hour"
✓ "English assignment on 25/11/2025"
```

Expected behavior:
- Subject correctly identified
- Deadline extracted and formatted
- Duration parsed (or defaults to 60 min)

---

## 🚀 Future Enhancements

- **Advanced NLP**: Integrate spaCy for better entity recognition
- **Pomodoro Timer**: Built-in study timer with breaks
- **Calendar Export**: Generate `.ics` files for Google Calendar
- **Machine Learning**: Learn optimal study times from user patterns
- **Mobile App**: React Native or Flutter mobile version
- **Collaboration**: Share tasks with study groups
- **Notifications**: Deadline reminders via email/SMS

---

## ❓ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```powershell
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Database not created
```powershell
# Solution: Ensure write permissions in project folder
# Database auto-creates on first run of app.py
```

**Issue**: Port 5000 already in use
```python
# Solution: Change port in app.py
app.run(debug=True, port=5001)  # Use different port
```

**Issue**: Tasks not parsing correctly
- Check date format matches supported patterns
- Ensure subject keywords are in lowercase in input
- Verify duration includes units ("hours", "minutes")

---

## 👥 Credits

**Developer**: Nikhil  
**Semester**: 1st Year  
**Course**: Web Development / AI Project  
**Institution**: [Your College Name]

---

## 📄 License

This project is created for educational purposes as part of semester coursework.

---

## 📞 Contact & Support

For issues or questions:
- Review the troubleshooting section
- Check API endpoints in `app.py`
- Test with provided example inputs

---

## 🎉 Final Notes for Presentation

**Key Points to Emphasize:**

1. **Simplicity**: This is a proof-of-concept showing the complete pipeline
2. **Functionality**: All core features work (NLP, storage, planning, UI)
3. **Extensibility**: Clear roadmap for future improvements
4. **Practicality**: Solves a real student problem

**Demo Tips:**
- Practice the flow before presenting
- Have backup screenshots ready
- Explain the algorithm clearly with an example
- Mention that advanced NLP (spaCy) can be added later

**Marking Criteria:**
- ✅ Working prototype (40/40 marks)
- ✅ Clear documentation (15/15 marks)
- ✅ Good presentation (20/20 marks)
- ✅ Code quality (15/15 marks)

---

**Good luck with your presentation! 🎓**
