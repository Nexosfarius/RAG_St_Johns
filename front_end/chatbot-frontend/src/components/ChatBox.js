import React, { useState } from 'react';
import './ChatBoxStyle.css';

function ChatBox() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);

    // Handles sending a message to the backend
    const sendMessage = async () => {
        if (input.trim() === '') return;

        const userMessage = { sender: "User", text: input };
        setMessages([...messages, userMessage]);

        // Send the message and current chat history to the backend
        const response = await fetch('http://localhost:5001/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: input,
                chat_history: messages.map(msg => [msg.sender, msg.text])  // Format the history correctly
            })
        });
        const data = await response.json();

        const botMessage = { sender: "Chatbot", text: data.answer };
        setMessages(prevMessages => [...prevMessages, botMessage]);

        setInput('');
    };

    return (
        <div className="chatbox">
            <div className="chatbox-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender.toLowerCase()}`}>
                        <strong>{msg.sender}: </strong> {msg.text}
                    </div>
                ))}
            </div>
            <div className="chatbox-input">
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatBox;
