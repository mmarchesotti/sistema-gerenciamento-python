$(document).ready(function () {
    getTasks();
    bindEvents();
});

const getTasks = _ => {
    $.ajax({
        url: "/tasks",
        method: "GET",
        success: (response) => {
            buildTasks(response.tasks);
        },
        error: _ => showToast("Algo deu errado ao recuperar os dados.", "danger"),
    });
}

const addTask = (title, description) => {
    $.ajax({
        url: "/tasks",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            title: title,
            description: description,
        }),
        success: (response) => {
            const newTask = {
                id: response.id,
                title: title,
                description: description,
                completed: false
            }
            buildTask(newTask);
        },
        error: _ => showToast("Algo deu errado ao cria a tarefa.", "danger"),
    });
}

const buildTasks = (tasks) => {
    for (let task of tasks) {
        buildTask(task);
    }
}

const buildTask = (task) => {
    const tasksContainer = $('#tasks-container');    
    const taskHtml = $(`            
        <div class="card m-2">
            <div class="card-body">
                <input type="checkbox" class="task-complete-checkbox"></input>
                ${task.title}
            </div>
        </div>
    `)
    tasksContainer.append(taskHtml);
}

const showToast = (message, type) => {
    $("#toastMessage").text(message);
    $("#resultToast").removeClass("bg-primary bg-success bg-danger").addClass(`bg-${type}`);
    
    const toastElement = document.getElementById("resultToast");
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
};

const showAddModal = _ => {    
    const modalElement = document.getElementById("addTaskModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
};

const bindEvents = _ => {
    const addTaskButton = $('#add-task-button');
    addTaskButton.on('click', _ => {
        showAddModal();
    });

    $("#add-task-btn").on('click', _ => {
        const title = $("#new-task-title-input").val();
        const description = $("#new-task-description-input").val();
        console.log(title)
        console.log(description)
        addTask(title, description);
    })
}