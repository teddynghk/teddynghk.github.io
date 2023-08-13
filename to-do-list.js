var taskList = [];
function addTask() {
    var taskInput = document.getElementById('taskInput');
    var taskContent = taskInput.value.trim();
    if (taskContent !== '') {
        taskList.push({ content: taskContent, completed: false });
        taskInput.value = '';
        displayTasks();
    }
}
function displayTasks() {
    var taskListElement = document.getElementById('taskList');
    taskListElement.innerHTML = '';
    taskList.forEach(function (task) {
        var listItem = document.createElement('li');
        listItem.className = 'task-item'; // Apply the 'task-item' class for styling
        var label = document.createElement('label');
        var checkboxText = document.createElement('span');
        checkboxText.textContent = "Undone";
        label.appendChild(checkboxText);
        listItem.appendChild(label);
        var taskContent = document.createElement('span');
        taskContent.textContent = task.content;
        listItem.appendChild(taskContent);
        if (task.completed) {
            taskContent.classList.add('completed');
            checkboxText.classList.add('done');
            checkboxText.textContent = "Done";
        }
        checkboxText.addEventListener('click', function () {
            task.completed = !task.completed;
            if (task.completed) {
                checkboxText.textContent = "Done";
                taskContent.classList.add('completed');
                checkboxText.classList.remove('undone');
                checkboxText.classList.add('done');
            }
            else {
                checkboxText.textContent = "Undone";
                taskContent.classList.remove('completed');
                checkboxText.classList.remove('done');
                checkboxText.classList.add('undone');
            }
        });
        taskListElement.appendChild(listItem);
    });
}
// Users press "Enter" to enter a new task
var taskInput = document.getElementById('taskInput');
taskInput.addEventListener("keydown", function (event) {
    if (event.isComposing || event.key === "Enter") {
        addTask();
    }
    // do something
});
var addButton = document.getElementById('addButton');
addButton.addEventListener('click', addTask);
displayTasks();