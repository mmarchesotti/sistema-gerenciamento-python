$(document).ready(function () {
    getTasks();
    bindGeneralEvents();
});

const getTasks = _ => {
    $.ajax({
        url: "/tasks",
        method: "GET",
        success: (response) => {
            buildTasks(response.tasks);
        },
        error: _ => {
            showToast("Algo deu errado ao recuperar os dados.", "danger")
        }
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
            showToast(response.message, "success");

            const newTask = {
                id: response.id,
                title: title,
                description: description,
                completed: false
            }
            buildTask(newTask);
        },
        error: _ => {
            showToast("Algo deu errado ao criar a tarefa.", "danger")
        }
    });
}

const updateTask = (id, title, description) => {
    $.ajax({
        url: `/tasks/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify({
            title: title,
            description: description,
        }),
        success: (response) => {
            showToast(response.message, "success");

            const taskCard = $(`.task-card[data-id=${id}]`);

            let task = taskCard.data("task");
            task.title = title;
            task.description = description;
            taskCard.data("task", task);

            taskCard.find(".task-card-title").text(title);
        },
        error: _ => {
            showToast("Algo deu errado ao atualizar a tarefa.", "danger")
        }
    });
}

const deleteTask = (id) => {
    $.ajax({
        url: `/tasks/${id}`,
        method: "DELETE",
        success: (response) => {
            showToast(response.message, "success");

            const taskCard = $(`.task-card[data-id=${id}]`);
            taskCard.remove();
        },
        error: _ => {
            showToast("Algo deu errado ao excluir a tarefa.", "danger")
        }
    });
}

const setCompleted = (id, completed) => {
    $.ajax({
        url: `/setCompleted/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify({
            completed: completed,
        }),
        success: (response) => {
            showToast(response.message, "success");

            const taskCard = $(`.task-card[data-id=${id}]`);

            let task = taskCard.data("task");
            task.completed = completed;
            taskCard.data("task", task);

            completed ? completeTaskCard(taskCard) : uncompleteTaskCard(taskCard);
        },
        error: _ => {
            showToast("Algo deu errado ao atualizar a tarefa.", "danger")
        }
    });
}

const completeTaskCard = (taskCard) => {
    taskCardTitle = taskCard.find(".task-card-title");
    taskCardCheckbox = taskCard.find(".task-completed-checkbox");
    
    taskCardTitle.css("text-decoration", "line-through");
    taskCardTitle.addClass("text-muted");
    taskCardCheckbox.prop("checked", true);
}

const uncompleteTaskCard = (taskCard) => {
    taskCardTitle = taskCard.find(".task-card-title");
    taskCardCheckbox = taskCard.find(".task-completed-checkbox");

    taskCardTitle.css("text-decoration", "none");    
    taskCardTitle.removeClass("text-muted");
    taskCardCheckbox.prop("checked", false);
}

const buildTasks = (tasks) => {
    for (let task of tasks) {
        const taskCard = buildTask(task);
        if (task.completed) completeTaskCard(taskCard);
    }
}

const buildTask = (task) => {
    const tasksContainer = $("#tasks-container");    
    const taskCard = $(`
        <div class="task-card card m-2" data-id=${task.id}>
            <div class="card-body d-flex align-items-center">
                <input type="checkbox" class="task-completed-checkbox me-1"></input>
                <span class="task-card-title flex-grow-1">${task.title}</span>
                <button type="button" class="btn btn-light" id="edit-task-btn" title="Editar tarefa">
                    <i class="bi bi-pencil"></i>
                </button>
                <button type="button" class="btn btn-light" id="delete-task-btn" title="Excluir tarefa">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
        </div>
    `).appendTo(tasksContainer);

    taskCard.data("task", task);
    taskCard.data("id", task.id);
    bindTaskCardEvents(taskCard)

    return taskCard;
}

const showToast = (message, type) => {
    $("#toastMessage").text(message);
    $("#resultToast").removeClass("bg-primary bg-success bg-danger").addClass(`bg-${type}`);
    
    const toastElement = document.getElementById("resultToast");
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
};

const showAddModal = _ => {
    $("#new-task-title-input").val("");
    $("#new-task-description-input").val("");

    const modalElement = document.getElementById("addTaskModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
};

const bindGeneralEvents = _ => {
    $("#add-task-button").on("click", _ => {
        showAddModal();
    });

    $("#add-task-btn").on("click", _ => {
        const title = $("#new-task-title-input").val();
        const description = $("#new-task-description-input").val();
        addTask(title, description);
    });

    $("#save-task-btn").on("click", _ => {
        const id = $("#updateTaskModal").data("id");
        const title = $("#edit-task-title-input").val();
        const description = $("#edit-task-description-input").val();
        updateTask(id, title, description);
    });
}

const bindTaskCardEvents = (selector) => {
    $(selector).find("#edit-task-btn").on("click", event => {
        const taskCard = $(event.currentTarget).closest(".task-card");
        const task = taskCard.data("task");
        showEditModal(task);
    });
    
    $(selector).find("#delete-task-btn").on("click", event => {
        const taskCard = $(event.currentTarget).closest(".task-card");
        const task = taskCard.data("task");
        const id = task.id;
        deleteTask(id);
    });
    
    $(selector).find(".task-completed-checkbox").on("click", event => {
        const checkbox = $(event.currentTarget);
        const taskCard = checkbox.closest(".task-card");
        const task = taskCard.data("task");
        const id = task.id;
        const completed = checkbox.is(":checked");
        setCompleted(id, completed);
    });
}

const showEditModal = (task) => {
    $("#updateTaskModal").data("id", task.id);
    $("#edit-task-title-input").val(task.title);
    $("#edit-task-description-input").val(task.description);

    const modalElement = document.getElementById("updateTaskModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}