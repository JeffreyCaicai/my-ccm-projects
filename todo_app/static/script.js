document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todoInput');
    const addBtn = document.getElementById('addBtn');
    const todoList = document.getElementById('todoList');
    const emptyState = document.getElementById('emptyState');
    const dateDisplay = document.getElementById('dateDisplay');

    // Display formatted date
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateDisplay.textContent = new Date().toLocaleDateString('en-US', options);

    // Fetch and render initial state
    fetchTodos();

    // Event Listeners
    addBtn.addEventListener('click', addTodo);
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTodo();
    });

    async function fetchTodos() {
        try {
            const response = await fetch('/api/todos');
            const todos = await response.json();
            renderTodos(todos);
        } catch (error) {
            console.error('Error fetching todos:', error);
        }
    }

    async function addTodo() {
        const content = todoInput.value.trim();
        if (!content) return;

        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content })
            });

            if (response.ok) {
                todoInput.value = '';
                fetchTodos();
            }
        } catch (error) {
            console.error('Error adding todo:', error);
        }
    }

    async function toggleTodo(id, currentStatus) {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ completed: !currentStatus })
            });

            if (response.ok) fetchTodos();
        } catch (error) {
            console.error('Error toggling todo:', error);
        }
    }

    async function deleteTodo(id) {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) fetchTodos();
        } catch (error) {
            console.error('Error deleting todo:', error);
        }
    }

    function renderTodos(todos) {
        todoList.innerHTML = '';

        if (todos.length === 0) {
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');

            todos.forEach(todo => {
                const li = document.createElement('li');
                li.className = `todo-item ${todo.completed ? 'completed' : ''}`;

                li.innerHTML = `
                    <div class="todo-content">
                        <div class="custom-checkbox">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="text">${escapeHtml(todo.content)}</span>
                    </div>
                    <button class="delete-btn">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                `;

                // Event Listeners for dynamic elements
                const contentDiv = li.querySelector('.todo-content');
                contentDiv.addEventListener('click', () => toggleTodo(todo.id, todo.completed));

                const deleteBtn = li.querySelector('.delete-btn');
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation(); // Prevent toggling when clicking delete
                    // Add fade out animation
                    li.style.transform = 'translateX(100px)';
                    li.style.opacity = '0';
                    setTimeout(() => deleteTodo(todo.id), 200);
                });

                todoList.appendChild(li);
            });
        }
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
