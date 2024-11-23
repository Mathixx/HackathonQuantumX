import React, { useState, useRef, useEffect } from "react";

function ChatBox() {
  const [messages, setMessages] = useState([]); // State to store messages
  const [input, setInput] = useState(""); // State for the current input message
  const messagesEndRef = useRef(null); // Create a ref for the messages container

  // Scroll to the bottom whenever messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Function to handle sending a message   
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();  // Call handleSend if Enter is pressed
    }
  };

  const handleSend = async () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, sender: "user" }];
      setMessages(newMessages);
      setInput("");

      try {
        // Send the message to the Python back-end (e.g., Flask)
        const response = await fetch("http://localhost:5000/send-message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: input }), // Sending the user's message to Python
        });

        if (response.ok) {
          // Get the bot's response and update the messages state
          const data = await response.json();
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: data.response, sender: "bot" },
          ]);
        } else {
          console.error("Error sending message to Python:", response.statusText);
        }
      } catch (error) {
        console.error("Error connecting to the server:", error);
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
        {/* Invisible element to ensure scrolling to the latest message */}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)} // Update input state
          onKeyDown={handleKeyPress}  // Listen for Enter key
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default ChatBox;
