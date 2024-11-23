import React, { useState } from "react";
import Tabs from "./Tabs";
import ChatBox from "./ChatBox";
import Orders from "./Orders";  // Import Orders
import ProductList from "./ProductList";  // Import ProductList
import Basket from "./Basket";  // Import Basket
import "./App.css";

function App() {

  const [activeTab, setActiveTab] = useState('products'); // For tab navigation
  const [updateTrigger, setUpdateTrigger] = useState(false); // Trigger for ProductList update

  // Function to trigger product update
  const triggerProductUpdate = () => {
    setUpdateTrigger((prev) => !prev); // Toggle the update trigger state
  };

  return (
    <div className="app-container">
      {/* Right Side */}
      <div className="left-panel">
        <ChatBox triggerProductUpdate={triggerProductUpdate} /> {/* Pass function to ChatBox */}
      </div>

      {/* Left Side */}
      <div className="right-panel">
        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
        
        {activeTab === "products" && <ProductList updateTrigger={updateTrigger} />}  {/* Pass trigger to ProductList */}
        {activeTab === "basket" && <Basket />}
        {activeTab === "orderHistory" && <Orders />}
      </div>
    </div>
  );
}

export default App;
