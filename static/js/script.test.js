/**
 * @jest-environment jsdom
 */
const $ = require("jquery");
global.$ = $;

const { JSDOM } = require("jsdom");
const dom = new JSDOM(`
<!DOCTYPE html>
<html>
    <body>
        <div id="tasks-container"></div>
        <div id="resultToast" class="toast"></div>
        <input id="new-task-title-input" />
        <input id="new-task-description-input" />
    </body>
</html>`);
global.document = dom.window.document;
global.window = dom.window;

require("./script");

describe("Task Management Tests", () => {
    beforeEach(() => {
        $("#tasks-container").empty();
    });

    test("buildTask should add a task to the DOM", () => {
        const task = { id: 1, title: "Test Task", description: "Test Description", completed: false };
        buildTask(task);

        const taskCard = $("#tasks-container .task-card[data-id='1']");
        expect(taskCard.length).toBe(1);
        expect(taskCard.find(".task-card-title").text()).toBe("Test Task");
    });

    test("completeTaskCard should style a completed task", () => {
        const task = { id: 2, title: "Complete Task", description: "", completed: true };
        const taskCard = buildTask(task);
        completeTaskCard(taskCard);

        expect(taskCard.find(".task-card-title").css("text-decoration")).toBe("line-through");
        expect(taskCard.find(".task-card-title").hasClass("text-muted")).toBe(true);
    });

    test("addTask triggers a POST request", async () => {
        global.$.ajax = jest.fn((options) => {
            if (options.method === "POST") {
                options.success({ message: "Tarefa criada com sucesso!", id: 1 });
            }
        });

        addTask("New Task", "Task Description");

        expect($.ajax).toHaveBeenCalledWith(
            expect.objectContaining({
                url: "/tasks",
                method: "POST",
                data: JSON.stringify({ title: "New Task", description: "Task Description" }),
            })
        );
    });

    test("showToast displays the toast with the correct message", () => {
        showToast("Test Message", "success");

        const toast = $("#resultToast");
        expect(toast.hasClass("bg-success")).toBe(true);
        expect($("#toastMessage").text()).toBe("Test Message");
    });
});
