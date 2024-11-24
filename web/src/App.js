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

  // Function to trigger product and basket updates
  const triggerProductAndBasketUpdate = () => {
    setUpdateTrigger((prev) => !prev); // Toggle the update trigger state
  };

  return (
    <div className="app-container">
      {/* Left Side */}
      <div className="left-panel">
        <ChatBox triggerProductUpdate={triggerProductAndBasketUpdate} /> {/* Pass trigger to ChatBox */}
      </div>

      {/* Right Side */}
      <div className="right-panel">
        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

        {activeTab === "products" && <ProductList updateTrigger={updateTrigger} />} {/* Pass trigger to ProductList */}
        {activeTab === "basket" && <Basket updateTrigger={updateTrigger} />} {/* Pass trigger to Basket */}
        {activeTab === "orderHistory" && <Orders />}
      </div>
    </div>
  );
}

export default App;
