from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Use SQLite for simplicity
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'todos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'completed': self.completed
        }

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    new_todo = Todo(content=data['content'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    
    if 'completed' in data:
        todo.completed = data['completed']
    if 'content' in data:
        todo.content = data['content']
        
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
