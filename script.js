// script.js

// Array of dialogue lines
const dialogues = [
    "This is the first line of dialogue.",
    "Here’s the second line with more information.",
    "Another line of dialogue, moving the story forward.",
    "Final line of dialogue for this sequence."
];

let currentDialogueIndex = 0;

function nextDialogue() {
    if (currentDialogueIndex < dialogues.length - 1) {
        // Update the dialogue text with the next line
        currentDialogueIndex++;
        document.getElementById("dialogue-text").innerText = dialogues[currentDialogueIndex];
    } else {
        document.getElementById("dialogue-box").style.display = "None";
        console.log('hello testing')
        const buttonContainer = document.querySelector(".button-container");
        buttonContainer.innerHTML = '<input type="text" class="user-input" placeholder="Type your response..." />';
    }
}
