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
    }
}
