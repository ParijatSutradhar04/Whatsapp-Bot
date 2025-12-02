// app.js - exact-like behavior: append messages, show double ticks, typing indicator, auto-scroll

const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

function nowTs() {
  const d = new Date();
  return d.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
}

function createTickSVG() {
  // two grey ticks (not blue)
  return `
    <svg class="tick" viewBox="0 0 16 12" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M1 6.5L4 9.5L7.5 2" stroke="#92a3ad" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M6 6.5L9 9.5L14 3" stroke="#92a3ad" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `;
}

function appendIncoming(text) {
  const wrap = document.createElement('div');
  wrap.className = 'msg-wrapper left';
  wrap.innerHTML = `
    <div class="bubble">
      <div class="msg-text">${escapeHtml(text)}</div>
      <div class="meta"><span class="time">${nowTs()}</span></div>
    </div>
  `;
  chat.appendChild(wrap);
  scrollBottom();
}

function appendOutgoing(text) {
  const wrap = document.createElement('div');
  wrap.className = 'msg-wrapper right';
  wrap.innerHTML = `
    <div class="bubble">
      <div class="msg-text">${escapeHtml(text)}</div>
      <div class="meta"><span class="time">${nowTs()}</span>${createTickSVG()}</div>
    </div>
  `;
  chat.appendChild(wrap);
  scrollBottom();
}

function showTyping() {
  removeTyping();
  const t = document.createElement('div');
  t.className = 'msg-wrapper left';
  t.id = 'typing';
  t.innerHTML = `
    <div class="bubble">
      <div class="typing">
        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
      </div>
    </div>
  `;
  chat.appendChild(t);
  scrollBottom();
}

function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

function scrollBottom() {
  // ensure newest message visible
  setTimeout(() => {
    chat.scrollTo({ top: chat.scrollHeight + 200, behavior: 'smooth' });
  }, 40);
}

// escape html
function escapeHtml(unsafe) {
  return unsafe
       .replace(/&/g, "&amp;")
       .replace(/</g, "&lt;")
       .replace(/>/g, "&gt;")
       .replace(/"/g, "&quot;")
       .replace(/'/g, "&#039;");
}

// send to backend
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  appendOutgoing(text);
  input.value = "";
  showTyping();

  try {
    const res = await fetch('/api/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ message: text })
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(err || 'server error');
    }
    const data = await res.json();
    removeTyping();
    appendIncoming(data.reply || '(no reply)');
  } catch (err) {
    removeTyping();
    appendIncoming('Error: ' + err.message);
    console.error(err);
  }
}

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendMessage();
  }
});

// small typing animation css-in-js (for incoming typing dots)
const style = document.createElement('style');
style.innerHTML = `
.typing{ display:flex; gap:6px; align-items:center; }
.dot{ width:7px; height:7px; border-radius:50%; background: #8696A0; opacity:0.9; animation: blink 1.2s infinite; }
.dot:nth-child(2){ animation-delay:0.15s } .dot:nth-child(3){ animation-delay:0.3s }
@keyframes blink{ 0%{ transform:translateY(0); opacity:0.25 } 50%{ transform:translateY(-4px); opacity:1 } 100%{ transform:translateY(0); opacity:0.25 } }
`;
document.head.appendChild(style);

// Dynamic height adjustment for phone container
function setPhoneHeight() {
  const phone = document.querySelector('.phone');
  if (!phone) return;
  
  const viewportHeight = window.innerHeight;
  const maxHeight = Math.min(viewportHeight * 0.98, 850); // 98% of viewport or 850px max
  const minHeight = 500; // minimum height
  
  const calculatedHeight = Math.max(minHeight, maxHeight);
  phone.style.height = `${calculatedHeight}px`;
  phone.style.maxHeight = `${calculatedHeight}px`;
}

// Set height on load and resize
setPhoneHeight();
window.addEventListener('resize', setPhoneHeight);
window.addEventListener('orientationchange', setPhoneHeight);

// initial focus
input.focus();
