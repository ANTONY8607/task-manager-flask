from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Task, db
from datetime import datetime, timedelta
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    # Récupérer les paramètres de filtrage et de tri
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    priority = request.args.get('priority', '')
    status = request.args.get('status', '')
    sort = request.args.get('sort', 'due_date')
    order = request.args.get('order', 'asc')

    # Construire la requête de base
    query = Task.query.filter_by(user_id=current_user.id)

    # Appliquer les filtres
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%')
            )
        )
    if category:
        query = query.filter_by(category=category)
    if priority:
        query = query.filter_by(priority=priority)
    if status:
        completed = status == 'completed'
        query = query.filter_by(completed=completed)

    # Appliquer le tri
    if sort == 'title':
        query = query.order_by(Task.title.asc() if order == 'asc' else Task.title.desc())
    elif sort == 'priority':
        query = query.order_by(Task.priority.asc() if order == 'asc' else Task.priority.desc())
    elif sort == 'category':
        query = query.order_by(Task.category.asc() if order == 'asc' else Task.category.desc())
    else:  # default: due_date
        query = query.order_by(Task.due_date.asc() if order == 'asc' else Task.due_date.desc())

    tasks = query.all()
    
    # Récupérer les catégories et priorités uniques pour les filtres
    categories = db.session.query(Task.category).distinct().all()
    priorities = db.session.query(Task.priority).distinct().all()

    return render_template('index.html', 
                         tasks=tasks,
                         categories=categories,
                         priorities=priorities,
                         current_category=category,
                         current_priority=priority,
                         current_status=status,
                         current_sort=sort,
                         current_order=order,
                         search=search)

@main.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M')
        priority = request.form.get('priority')
        category = request.form.get('category')

        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!')
        return redirect(url_for('main.index'))

    return render_template('task/new.html')

@main.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M')
        task.priority = request.form.get('priority')
        task.category = request.form.get('category')
        
        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('main.index'))

    return render_template('task/edit.html', task=task)

@main.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('main.index'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('main.index'))

@main.route('/task/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('main.index'))

    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/calendar')
@login_required
def calendar():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    events = []
    for task in tasks:
        event = {
            'id': task.id,
            'title': task.title,
            'start': task.due_date.isoformat(),
            'description': task.description,
            'priority': task.priority,
            'category': task.category,
            'completed': task.completed,
            'backgroundColor': '#ffffff',
            'borderColor': '#dc3545' if task.priority == 'Haute' 
                          else '#ffc107' if task.priority == 'Moyenne'
                          else '#0dcaf0',
            'textColor': '#000000',
            'className': 'task-event' + (' completed' if task.completed else '')
        }
        events.append(event)
    return render_template('calendar.html', events=events)

@main.route('/api/tasks')
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    events = []
    for task in tasks:
        event = {
            'id': task.id,
            'title': task.title,
            'start': task.due_date.isoformat(),
            'description': task.description,
            'priority': task.priority,
            'category': task.category,
            'completed': task.completed,
            'backgroundColor': '#ffffff',
            'borderColor': '#dc3545' if task.priority == 'Haute' 
                          else '#ffc107' if task.priority == 'Moyenne'
                          else '#0dcaf0',
            'textColor': '#000000',
            'className': 'task-event' + (' completed' if task.completed else '')
        }
        events.append(event)
    return jsonify(events)
