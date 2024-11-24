import React, { useState, useRef, useEffect } from "react";

function ChatBox({ triggerUpdate }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const fetchInitialMessage = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/init-message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          setMessages([{ text: data.response, sender: "bot" }]);
        } else {
          console.error("Failed to fetch initial message:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching initial message:", error);
      }
    };

    fetchInitialMessage();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: "user" }]);
      setInput("");
      setIsLoading(true);

      try {
        const response = await fetch("http://127.0.0.1:5000/send-message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: input }),
        });

        if (response.ok) {
          const data = await response.json();

          // Update chat messages
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: data.response, sender: "bot" },
          ]);

          // Trigger the update for cart and product list
          triggerUpdate();
        } else {
          console.error("Error sending message to Python:", response.statusText);
        }
      } catch (error) {
        console.error("Error connecting to the server:", error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="chat-box">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            <span className="chat-sender">{msg.sender}:</span> {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
