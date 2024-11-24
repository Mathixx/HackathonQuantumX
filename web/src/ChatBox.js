import React, { useState, useRef, useEffect } from "react";
import ProductList from "./ProductList"; // Import the ProductList component

function ChatBox({ triggerProductUpdate }) {
  const [messages, setMessages] = useState([]); // State to store messages
  const [input, setInput] = useState(""); // State for the current input message
  const [isLoading, setIsLoading] = useState(false); // State to track if a response is pending
  const messagesEndRef = useRef(null); // Create a ref for the messages container

  // Fetch the initial message when the component mounts
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
          setMessages([{ text: data.response, sender: "bot" }]); // Initialize with bot message
        } else {
          console.error("Failed to fetch initial message:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching initial message:", error);
      }
    };

    fetchInitialMessage();
  }, []); // Empty dependency array ensures this runs only once when the component mounts

  // Scroll to the bottom whenever messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Function to handle sending a message
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !isLoading) {
      handleSend(); // Call handleSend if Enter is pressed and not loading
    }
  };

  const handleSend = async () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, sender: "user" }];
      setMessages(newMessages);
      setInput("");
      setIsLoading(true); // Disable input and button while waiting for a response

      try {
        // Send the message to the Python back-end (e.g., Flask)
        const response = await fetch("http://127.0.0.1:5000/send-message", {
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
          triggerProductUpdate();
        } else {
          console.error("Error sending message to Python:", response.statusText);
        }
      } catch (error) {
        console.error("Error connecting to the server:", error);
      } finally {
        setIsLoading(false); // Re-enable input and button when the response is received
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
          onKeyDown={handleKeyPress} // Listen for Enter key
          placeholder="Type your message..."
          disabled={isLoading} // Disable input while loading
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"} {/* Change button text while loading */}
        </button>
      </div>
    </div>
  );
}

export default ChatBox;

