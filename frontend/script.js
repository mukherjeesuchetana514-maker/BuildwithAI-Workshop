document.addEventListener('DOMContentLoaded', () => {
    const chatToggleBtn = document.getElementById('chat-toggle-btn');
    const closeChatBtn = document.getElementById('close-chat-btn');
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // Toggle Chat Window
    const toggleChat = () => {
        if (chatWindow.classList.contains('hidden')) {
            // Open
            chatWindow.classList.remove('hidden');
            // Add a tiny delay to allow display:block to apply before animating opacity/scale
            setTimeout(() => {
                chatWindow.classList.remove('scale-95', 'opacity-0');
                chatWindow.classList.add('scale-100', 'opacity-100');
            }, 10);
            chatInput.focus();
        } else {
            // Close
            chatWindow.classList.remove('scale-100', 'opacity-100');
            chatWindow.classList.add('scale-95', 'opacity-0');
            setTimeout(() => {
                chatWindow.classList.add('hidden');
            }, 300); // match transition duration
        }
    };

    chatToggleBtn.addEventListener('click', toggleChat);
    closeChatBtn.addEventListener('click', toggleChat);

    // Add Message to UI
    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex flex-col space-y-1 max-w-[85%] ${sender === 'user' ? 'self-end' : 'self-start'}`;
        
        const senderLabel = document.createElement('span');
        senderLabel.className = `text-xs text-gray-500 ${sender === 'user' ? 'mr-1 self-end' : 'ml-1'}`;
        senderLabel.innerText = sender === 'user' ? 'You' : 'Assistant';
        
        const bubble = document.createElement('div');
        if (sender === 'user') {
            bubble.className = 'bg-black text-white rounded-2xl rounded-tr-sm px-4 py-2 text-sm shadow-sm break-words';
        } else {
            bubble.className = 'bg-gray-200 text-gray-800 rounded-2xl rounded-tl-sm px-4 py-2 text-sm shadow-sm break-words';
        }
        bubble.innerText = text;

        messageDiv.appendChild(senderLabel);
        messageDiv.appendChild(bubble);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Handle Form Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message to UI
        addMessage(message, 'user');
        chatInput.value = '';

        // Show loading indicator
        const loadingId = 'loading-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.id = loadingId;
        loadingDiv.className = 'flex flex-col space-y-1 max-w-[85%] self-start';
        loadingDiv.innerHTML = `
            <span class="text-xs text-gray-500 ml-1">Assistant</span>
            <div class="bg-gray-200 text-gray-800 rounded-2xl rounded-tl-sm px-4 py-3 text-sm shadow-sm flex items-center space-x-1">
                <div class="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                <div class="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
        `;
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove loading indicator
            document.getElementById(loadingId).remove();
            
            // Add bot reply
            addMessage(data.reply, 'bot');
            
        } catch (error) {
            console.error('Error:', error);
            document.getElementById(loadingId).remove();
            addMessage('Sorry, I am having trouble connecting to the server right now.', 'bot');
        }
    });
});
