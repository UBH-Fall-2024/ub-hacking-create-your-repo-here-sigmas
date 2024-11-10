// Array of dialogue lines
const dialogues = [
    "Welcome!",
    "Hop in! Let's turn your story into a comic adventure!",
    "Another line of dialogue, moving the story forward.",
    "Final line of dialogue for this sequence."
];

let currentDialogueIndex = 0;

function nextDialogue() {
    currentDialogueIndex++;
    if (currentDialogueIndex < dialogues.length) {
        // Update the dialogue text with the next line
        document.getElementById("dialogue-text").innerText = dialogues[currentDialogueIndex];
    } else {
        // Hide the dialogue box once the dialogue sequence is complete
        document.getElementById("dialogue-box").style.display = "none";

        // Create a form container for user input
        const formContainer = document.createElement("div");
        formContainer.classList.add("form-container");

        // Add form title
        const formTitle = document.createElement("h1");
        formTitle.innerText = "Create Your Comic";

        // Create the form element
        const form = document.createElement("form");
        form.action = "/";
        form.method = "post";

        // Story Title Label and Input
        const titleLabel = document.createElement("label");
        titleLabel.for = "story_title";
        titleLabel.innerText = "Story Title:";
        const titleInput = document.createElement("input");
        titleInput.type = "text";
        titleInput.id = "story_title";
        titleInput.name = "story_title";
        titleInput.required = true;

        // Story Outline Label and Textarea
        const outlineLabel = document.createElement("label");
        outlineLabel.for = "story_outline";
        outlineLabel.innerText = "Story Outline:";
        const outlineTextarea = document.createElement("textarea");
        outlineTextarea.id = "story_outline";
        outlineTextarea.name = "story_outline";
        outlineTextarea.rows = 6;
        outlineTextarea.cols = 40;
        outlineTextarea.required = true;

        // Submit Button
        const submitButton = document.createElement("button");
        submitButton.type = "submit";
        submitButton.innerText = "Generate Comic";

        // Append elements to form
        form.appendChild(titleLabel);
        form.appendChild(document.createElement("br"));
        form.appendChild(titleInput);
        form.appendChild(document.createElement("br"));
        form.appendChild(document.createElement("br"));
        form.appendChild(outlineLabel);
        form.appendChild(document.createElement("br"));
        form.appendChild(outlineTextarea);
        form.appendChild(document.createElement("br"));
        form.appendChild(document.createElement("br"));
        form.appendChild(submitButton);

        // Append form and title to the form container
        formContainer.appendChild(formTitle);
        formContainer.appendChild(form);

        // Append the form container to the body
        document.body.appendChild(formContainer);
    }
}
