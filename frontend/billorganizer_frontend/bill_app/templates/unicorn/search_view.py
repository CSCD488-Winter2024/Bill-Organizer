<!-- unicorn/templates/unicorn/todo.html -->
<div>
    <form unicorn:submit.prevent="add">
        <input type="text" unicorn:model.lazy="task" placeholder="New task" id="task"></input>
    </form>
    <button unicorn:click="add">Add</button>

    <p>
        {% if tasks %}
        <ul>
            {% for task in tasks %}
            <li>{{ task }}</li>
            {% endfor %}
        </ul>

        <button unicorn:click="$reset">Clear all tasks</button>
        {% else %}
        No tasks 🎉
        {% endif %}
    </p>
</div>