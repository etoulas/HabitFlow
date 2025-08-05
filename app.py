import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Data file path
DATA_FILE = 'data/habits.json'

def load_data():
    """Load habits data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"habits": []}
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return {"habits": []}

def save_data(data):
    """Save habits data to JSON file"""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        return False

def generate_id():
    """Generate a unique ID based on timestamp"""
    return str(int(datetime.now().timestamp() * 1000))

@app.route('/')
def index():
    """Main dashboard showing all habits"""
    data = load_data()
    habits = data.get('habits', [])
    
    # Calculate statistics for each habit
    today = datetime.now().strftime('%Y-%m-%d')
    for habit in habits:
        habit['today_completed'] = calculate_today_completion(habit, today)
        habit['streak'] = calculate_streak(habit)
        habit['total_completions'] = len(habit.get('completions', {}))
    
    return render_template('index.html', habits=habits, today=today)

@app.route('/add_habit', methods=['POST'])
def add_habit():
    """Add a new habit"""
    name = request.form.get('name', '').strip()
    frequency = request.form.get('frequency', 'daily')
    
    if not name:
        flash('Habit name is required', 'error')
        return redirect(url_for('index'))
    
    data = load_data()
    new_habit = {
        'id': generate_id(),
        'name': name,
        'frequency': frequency,
        'created_at': datetime.now().isoformat(),
        'tasks': [],
        'completions': {}  # date -> {task_id: completed, ...}
    }
    
    data['habits'].append(new_habit)
    
    if save_data(data):
        flash('Habit added successfully', 'success')
    else:
        flash('Error saving habit', 'error')
    
    return redirect(url_for('index'))

@app.route('/habit/<habit_id>')
def habit_detail(habit_id):
    """Show detailed view of a specific habit"""
    data = load_data()
    habit = next((h for h in data['habits'] if h['id'] == habit_id), None)
    
    if not habit:
        flash('Habit not found', 'error')
        return redirect(url_for('index'))
    
    # Generate calendar data for the last 30 days
    calendar_data = generate_calendar_data(habit, 30)
    
    return render_template('habit_detail.html', habit=habit, calendar_data=calendar_data)

@app.route('/add_task/<habit_id>', methods=['POST'])
def add_task(habit_id):
    """Add a task to a habit"""
    task_name = request.form.get('task_name', '').strip()
    task_size = request.form.get('task_size', 'small')
    
    if not task_name:
        flash('Task name is required', 'error')
        return redirect(url_for('habit_detail', habit_id=habit_id))
    
    data = load_data()
    habit = next((h for h in data['habits'] if h['id'] == habit_id), None)
    
    if not habit:
        flash('Habit not found', 'error')
        return redirect(url_for('index'))
    
    new_task = {
        'id': generate_id(),
        'name': task_name,
        'size': task_size,
        'created_at': datetime.now().isoformat()
    }
    
    habit['tasks'].append(new_task)
    
    if save_data(data):
        flash('Task added successfully', 'success')
    else:
        flash('Error saving task', 'error')
    
    return redirect(url_for('habit_detail', habit_id=habit_id))

@app.route('/toggle_task/<habit_id>/<task_id>', methods=['POST'])
def toggle_task(habit_id, task_id):
    """Toggle task completion for today"""
    data = load_data()
    habit = next((h for h in data['habits'] if h['id'] == habit_id), None)
    
    if not habit:
        flash('Habit not found', 'error')
        return redirect(url_for('index'))
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    if today not in habit['completions']:
        habit['completions'][today] = {}
    
    # Toggle task completion
    current_status = habit['completions'][today].get(task_id, False)
    habit['completions'][today][task_id] = not current_status
    
    if save_data(data):
        status = 'completed' if not current_status else 'uncompleted'
        flash(f'Task {status}', 'success')
    else:
        flash('Error updating task', 'error')
    
    return redirect(url_for('habit_detail', habit_id=habit_id))

@app.route('/delete_habit/<habit_id>', methods=['POST'])
def delete_habit(habit_id):
    """Delete a habit"""
    data = load_data()
    data['habits'] = [h for h in data['habits'] if h['id'] != habit_id]
    
    if save_data(data):
        flash('Habit deleted successfully', 'success')
    else:
        flash('Error deleting habit', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_task/<habit_id>/<task_id>', methods=['POST'])
def delete_task(habit_id, task_id):
    """Delete a task from a habit"""
    data = load_data()
    habit = next((h for h in data['habits'] if h['id'] == habit_id), None)
    
    if not habit:
        flash('Habit not found', 'error')
        return redirect(url_for('index'))
    
    # Remove task from habit
    habit['tasks'] = [t for t in habit['tasks'] if t['id'] != task_id]
    
    # Remove task completions from all dates
    for date_completions in habit['completions'].values():
        date_completions.pop(task_id, None)
    
    if save_data(data):
        flash('Task deleted successfully', 'success')
    else:
        flash('Error deleting task', 'error')
    
    return redirect(url_for('habit_detail', habit_id=habit_id))

def calculate_today_completion(habit, today):
    """Calculate completion percentage for today"""
    if not habit.get('tasks'):
        return 0
    
    today_completions = habit.get('completions', {}).get(today, {})
    completed_tasks = sum(1 for task in habit['tasks'] 
                         if today_completions.get(task['id'], False))
    
    return (completed_tasks / len(habit['tasks'])) * 100

def calculate_streak(habit):
    """Calculate current streak of days with any completion"""
    completions = habit.get('completions', {})
    if not completions:
        return 0
    
    streak = 0
    current_date = datetime.now().date()
    
    while True:
        date_str = current_date.strftime('%Y-%m-%d')
        day_completions = completions.get(date_str, {})
        
        # Check if any task was completed on this day
        if any(day_completions.values()):
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

def generate_calendar_data(habit, days=30):
    """Generate calendar data for the last N days"""
    calendar_data = []
    today = datetime.now().date()
    
    for i in range(days):
        date = today - timedelta(days=days - 1 - i)
        date_str = date.strftime('%Y-%m-%d')
        
        day_completions = habit.get('completions', {}).get(date_str, {})
        completed_tasks = []
        
        for task in habit.get('tasks', []):
            if day_completions.get(task['id'], False):
                completed_tasks.append({
                    'name': task['name'],
                    'size': task['size']
                })
        
        completion_percentage = 0
        if habit.get('tasks'):
            completion_percentage = (len(completed_tasks) / len(habit['tasks'])) * 100
        
        calendar_data.append({
            'date': date,
            'date_str': date_str,
            'completed_tasks': completed_tasks,
            'completion_percentage': completion_percentage,
            'is_today': date == today
        })
    
    return calendar_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
