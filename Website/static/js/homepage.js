var chatContainer = document.querySelector(".chat-container");
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function requestScrollToBottom() {
  requestAnimationFrame(scrollToBottom);
}

window.addEventListener("load", requestScrollToBottom);

document.getElementById("message-form").addEventListener("submit", function (event) {
  requestScrollToBottom();
});

const copyButtons = document.querySelectorAll(".copy-button");
copyButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const codeIndex = button.getAttribute("data-code");
    const codeElement = button.parentNode.querySelector("code");
    copyToClipboard(codeElement.innerText);
    button.innerText = "Copied!";
  });
});
function copyToClipboard(text) {
  const tempInput = document.createElement("textarea");
  tempInput.value = text;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand("copy");
  document.body.removeChild(tempInput);
}

const messageForm = document.getElementById("message-form");
const messageInput = document.getElementById("message-input");
const maxRows = 5;

function adjustTextareaHeight() {
  messageInput.style.height = "auto";
  messageInput.style.height = messageInput.scrollHeight + "px";
}

function checkRowCount() {
  const textareaRows = messageInput.value.split("\n").length;
  if (textareaRows > maxRows) {
    messageInput.style.overflowY = "scroll";
  } else {
    messageInput.style.overflowY = "auto";
  }
}
messageInput.addEventListener("input", () => {
  adjustTextareaHeight();
  checkRowCount();
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    messageForm.submit();
  }
});


adjustTextareaHeight();
checkRowCount();
