const messagesEl = document.getElementById("messages");
const form = document.getElementById("chatForm");
const input = document.getElementById("userInput");
const resetBtn = document.getElementById("resetBtn");

function addMessage(text, role) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";

  const typingEl = addMessage("Thinking…", "bot typing");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    typingEl.remove();
    if (data.error) {
      addMessage(`⚠️ ${data.error}`, "bot");
    } else {
      addMessage(data.reply, "bot");
    }
  } catch (err) {
    typingEl.remove();
    addMessage("⚠️ Network error. Please try again.", "bot");
  }
});

resetBtn.addEventListener("click", async () => {
  await fetch("/api/reset", { method: "POST" });
  messagesEl.innerHTML = "";
  addMessage("Conversation cleared. How can I help?", "bot");
});

addMessage("Hi! I'm richi your Ai assistant. Ask me anything.", "bot");
