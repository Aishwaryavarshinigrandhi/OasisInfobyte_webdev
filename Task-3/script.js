const taskInput = document.getElementById("taskInput");
const pendingList = document.getElementById("pendingList");
const completedList = document.getElementById("completedList");

function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText === "") return alert("Please enter a task");

    const li = createTaskElement(taskText, false);
    pendingList.appendChild(li);
    taskInput.value = "";
}

function createTaskElement(text, completed) {
    const li = document.createElement("li");

    const taskText = document.createElement("div");
    taskText.className = "task-text";
    taskText.innerText = text;

    const time = document.createElement("div");
    time.className = "task-time";
    time.innerText = `Added on: ${new Date().toLocaleString()}`;

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const completeBtn = document.createElement("button");
    completeBtn.className = "complete-btn";
    completeBtn.innerText = completed ? "Undo" : "Complete";

    completeBtn.onclick = () => {
        if (!completed) {
            completedList.appendChild(createTaskElement(text, true));
            li.remove();
        } else {
            pendingList.appendChild(createTaskElement(text, false));
            li.remove();
        }
    };

    const editBtn = document.createElement("button");
    editBtn.className = "edit-btn";
    editBtn.innerText = "Edit";
    editBtn.onclick = () => {
        const newText = prompt("Edit task", text);
        if (newText) {
            taskText.innerText = newText;
        }
    };

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-btn";
    deleteBtn.innerText = "Delete";
    deleteBtn.onclick = () => li.remove();

    actions.append(completeBtn, editBtn, deleteBtn);
    li.append(taskText, time, actions);

    return li;
}
