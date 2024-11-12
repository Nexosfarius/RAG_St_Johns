import React, { useState, useRef, useEffect } from 'react';
import './ChatBoxStyle.css';

function ChatBox() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const endOfMessagesRef = useRef(null);

    // Scroll to the bottom when messages change
    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Display typing indicator after a delay
    useEffect(() => {
        if (isLoading) {
            const timer = setTimeout(() => setIsTyping(true), 500); // Delay typing indicator by 500ms
            return () => clearTimeout(timer);
        } else {
            setIsTyping(false);
        }
    }, [isLoading]);

    // Typewriter effect for displaying text letter by letter
    const typewriterEffect = (text, callback) => {
        let index = 0;
        const interval = setInterval(() => {
            if (index < text.length) {
                callback(text.slice(0, index + 1));
                index++;
            } else {
                clearInterval(interval);
            }
        }, 50); // Adjust speed for letter appearance
    };

    const sendMessage = async () => {
        if (input.trim() === '' || isLoading) return;

        setIsLoading(true);
        const formattedDate = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const userMessage = { sender: "User", text: input, timestamp: formattedDate };
        setMessages([...messages, userMessage]);

        // Show "Thinking..." indicator
        const thinkingMessage = { sender: "Chatbot", text: "...", timestamp: formattedDate };
        setMessages(prevMessages => [...prevMessages, thinkingMessage]);

        try {
            const response = await fetch('http://localhost:5001/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: input,
                    chat_history: messages.map(msg => [msg.sender, msg.text])
                })
            });

            if (!response.ok) throw new Error("Server error");

            const data = await response.json();

            // Remove thinking indicator
            setMessages(prevMessages => prevMessages.slice(0, -1));

            // Add an empty bot message for typewriter effect
            const botMessage = { sender: "Chatbot", text: '', timestamp: formattedDate };
            setMessages(prevMessages => [...prevMessages, botMessage]);

            // Convert URLs into clickable links
            const formattedText = data.answer.replace(
                /(https?:\/\/\S+)/g,
                '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
            );

            // Apply typewriter effect for letter-by-letter appearance
            typewriterEffect(formattedText, text => {
                setMessages(prevMessages => {
                    const newMessages = [...prevMessages];
                    newMessages[newMessages.length - 1].text = text;
                    return newMessages;
                });
            });

        } catch (error) {
            // Handle errors and show error message in chat
            const errorMessage = { sender: "System", text: "Error: Unable to reach the server", timestamp: formattedDate };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        }

        setInput('');
        setIsLoading(false);
    };

    return (
        <div className="chatbox">
            <div className="chatbox-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender.toLowerCase()}`}>
                        <span dangerouslySetInnerHTML={{ __html: `<strong>${msg.sender}:</strong> ${msg.text}` }} />
                        <span className="timestamp">{msg.timestamp}</span>
                    </div>
                ))}
                {isTyping && (
                    <div className="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                )}
                <div ref={endOfMessagesRef}></div> {/* Auto-scroll anchor */}
            </div>
            <div className="chatbox-input">
                <input
                    type="text"
                    placeholder="Type your message..."
                    aria-label="Type your message"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    disabled={isLoading}
                />
                <button onClick={sendMessage} disabled={isLoading} aria-label="Send message">Send</button>
            </div>
        </div>
    );
}

export default ChatBox;