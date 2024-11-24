import React, { useState } from "react";
import Tabs from "./Tabs";
import ChatBox from "./ChatBox";
import Orders from "./Orders";
import ProductList from "./ProductList";
import Basket from "./Basket";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState('products'); // Track the active tab
  const [products, setProducts] = useState([]); // State for product list
  const [basket, setBasket] = useState([]); // State for basket

  // Fetch products when the "Products" tab is clicked
  const fetchProducts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/get-products", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        const data = await response.json();
        setProducts(data.products); // Update the products state
      } else {
        console.error("Failed to fetch products:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  // Fetch basket when the "Basket" tab is clicked
  const fetchBasket = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/get-cart", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        const data = await response.json();
        setBasket(data.cart); // Update the basket state
      } else {
        console.error("Failed to fetch cart:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching cart:", error);
    }
  };

  // Handle tab changes
  const handleTabChange = (tab) => {
    setActiveTab(tab);

    if (tab === "products") {
      fetchProducts(); // Trigger product fetch when Products tab is clicked
    } else if (tab === "basket") {
      fetchBasket(); // Trigger basket fetch when Basket tab is clicked
    }
  };

  return (
    <div className="app-container">
      {/* Left Side */}
      <div className="left-panel">
        <ChatBox />
      </div>

      {/* Right Side */}
      <div className="right-panel">
        <Tabs activeTab={activeTab} setActiveTab={handleTabChange} />

        {activeTab === "products" && <ProductList products={products} />}
        {activeTab === "basket" && <Basket basket={basket} />}
        {activeTab === "orderHistory" && <Orders />}
      </div>
    </div>
  );
}

export default App;