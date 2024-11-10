// script.js

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

         // Create a new input container
        const inputContainer = document.createElement("div");
        inputContainer.classList.add("input-container");

        // Create an input element
        const userInput = document.createElement("textarea");
        userInput.type = "text";
        userInput.classList.add("user-input");
        userInput.placeholder = "Type your response...";

        // Create an "Enter" button
        const enterButton = document.createElement("button");
        enterButton.classList.add("enter-btn");
        enterButton.innerText = "Enter";

        // Append the input and button to the container, and add the container to the body
        inputContainer.appendChild(userInput);
        inputContainer.appendChild(enterButton);
        document.body.appendChild(inputContainer);

        // Optional: Automatically focus the input field
        userInput.focus();
    }
}
