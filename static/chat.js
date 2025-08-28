document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("message-input");
    const chatBox = document.getElementById("chat-messages");
    const typingIndicator = document.getElementById("typing-indicator");
    let currentSessionId = null;
 
    function initializeSession() {
        currentSessionId = 'session_' + Math.random().toString(36).substr(2, 9);
        const sessionIdElement = document.getElementById('session-id');
        if (sessionIdElement) {
            sessionIdElement.textContent = currentSessionId;
        }
    }
    
    function formatAgentResponse(message) {
        // Detect response type
        if (message.includes('Flight') && message.includes('Duration:')) {
            // ...existing flight formatting code...
            const flightRegex = /\*\*Flight (\d+) \(ID: (\d+)\):\*\*\n\*\s+\*\*Duration:\*\* ([^\n]+)\n\*\s+\*\*Segments:\*\*\n((?:\s+\*\s+Departure:[^\n]+\n\s+\*\s+Arrival:[^\n]+\n\s+\*\s+Carrier:[^\n]+\n?)+)\*\s+\*\*Price:\*\* ([^\n]+) EUR/g;
            let flights = [];
            let match;
            while ((match = flightRegex.exec(message)) !== null) {
                flights.push({
                    num: match[1],
                    id: match[2],
                    duration: match[3],
                    segments: match[4],
                    price: match[5]
                });
            }
            if (flights.length > 0) {
                let html = '<div class="space-y-4">';
                flights.forEach(flight => {
                    html += `
                    <div class="rounded-lg shadow-md bg-white border border-blue-100 p-4">
                        <div class="flex items-center mb-2">
                            <i class="fas fa-plane text-blue-500 mr-2"></i>
                            <span class="font-bold text-lg">Flight ${flight.num}</span>
                            <span class="ml-2 text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded">ID: ${flight.id}</span>
                        </div>
                        <div class="text-sm text-gray-700 mb-1"><strong>Duration:</strong> ${flight.duration}</div>
                        <div class="mb-2">
                            <strong>Segments:</strong>
                            <ul class="list-disc list-inside text-gray-600 text-sm mt-1">
                                ${flight.segments.split('\n').filter(s => s.trim()).map(s => `<li>${s.replace(/^\s*\*\s*/, '')}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="text-right text-blue-700 font-semibold text-base">Price: ${flight.price} EUR</div>
                    </div>
                    `;
                });
                html += '</div>';
                return html;
            }
        }
        // Fallback: basic markdown formatting
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/• /g, '• ')
            .replace(/\n/g, '<br>');
    }
    
    function appendMessage(sender, message, cssClass = '') {
        const msgDiv = document.createElement("div");
        msgDiv.className = sender === "user" ? "message-bubble flex items-start space-x-3 flex-row-reverse space-x-reverse" : "message-bubble flex items-start space-x-3";
        let avatarClass = sender === "user" ? "bg-blue-500" : "bg-gray-400";
        let avatarIcon = sender === "user" ? "fas fa-user" : "fas fa-robot";
        let bubbleClass = sender === "user" ? "bg-blue-500 text-white ml-auto" : "bg-gray-100 text-gray-700";
        let maxWidth = "max-w-md" + (sender === "user" ? " ml-auto" : "");
        let content = sender === "assistant" ? formatAgentResponse(message) : message;
        msgDiv.innerHTML = `
            <div class="flex-shrink-0">
                <div class="w-8 h-8 ${avatarClass} rounded-full flex items-center justify-center text-white">
                    <i class="${avatarIcon} text-sm"></i>
                </div>
            </div>
            <div class="flex-1">
                <div class="${bubbleClass} rounded-lg p-3 ${maxWidth}">
                    <div class="whitespace-pre-wrap">${content}</div>
                </div>
                <div class="text-xs text-gray-500 mt-1 ${sender === "user" ? "text-right" : ""}">
                    ${sender === "user" ? "You" : "Assistant"}
                </div>
            </div>
        `;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return msgDiv;
    }

    chatForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;
        appendMessage("user", message);
        userInput.value = "";
        userInput.disabled = true;
        typingIndicator.classList.add("show");
        try {
            const response = await fetch("/chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message, session_id: currentSessionId })
            });
            const data = await response.json();
            if (data.session_id) {
                currentSessionId = data.session_id;
            }
            appendMessage("assistant", data.response);
        } catch (err) {
            appendMessage("assistant", "Error: Could not reach agent.");
        } finally {
            typingIndicator.classList.remove("show");
            userInput.disabled = false;
            userInput.focus();
        }
    });

    document.getElementById('clear-chat').addEventListener('click', () => {
        chatBox.innerHTML = `
            <div class="message-bubble flex items-start space-x-3">
                <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white">
                        <i class="fas fa-robot text-sm"></i>
                    </div>
                </div>
                <div class="flex-1">
                    <div class="bg-gray-100 rounded-lg p-3 max-w-md">
                        <p class="text-gray-700">Chat cleared! How can I help you today?</p>
                    </div>
                    <div class="text-xs text-gray-500 mt-1">Assistant</div>
                </div>
            </div>
        `;
        initializeSession();
    });
 
    initializeSession();
});