interface Task {
  content: string;
  completed: boolean;
}

const taskList: Task[] = [];

function addTask() {
  const taskInput = document.getElementById('taskInput') as HTMLInputElement;
  const taskContent = taskInput.value.trim();
  if (taskContent !== '') {
    taskList.push({ content: taskContent, completed: false });
    taskInput.value = '';
    displayTasks();
  }
}

function displayTasks() {
  const taskListElement = document.getElementById('taskList');
  taskListElement.innerHTML = '';
  taskList.forEach((task) => {
    const listItem = document.createElement('li');
    listItem.className = 'task-item'; // Apply the 'task-item' class for styling

    const label = document.createElement('label');

    const checkboxText = document.createElement('span');
    checkboxText.textContent = "Undone";
    label.appendChild(checkboxText);

    listItem.appendChild(label);

    const taskContent = document.createElement('span');
    taskContent.textContent = task.content;
    listItem.appendChild(taskContent);

    if (task.completed){
        taskContent.classList.add('completed');
        checkboxText.classList.add('done');
        checkboxText.textContent = "Done";
    }

    checkboxText.addEventListener('click', () => {
        task.completed = !task.completed;
        if (task.completed){
            checkboxText.textContent = "Done";
            taskContent.classList.add('completed');
            checkboxText.classList.remove('undone');
            checkboxText.classList.add('done');
        }
        else{
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
const taskInput = document.getElementById('taskInput') as HTMLInputElement;
taskInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        addTask();
    }
    // do something
  });

const addButton = document.getElementById('addButton');
addButton.addEventListener('click', addTask);

displayTasks();
