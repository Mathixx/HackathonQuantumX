import React, { useState, useEffect } from "react";
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

  // Fetch products from the server
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

  // Fetch basket from the server
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

  // Fetch products and basket every 10 seconds
  useEffect(() => {
    fetchProducts(); // Fetch products when the component mounts
    fetchBasket(); // Fetch basket when the component mounts

    // Set interval to fetch products and basket every 10 seconds
    const intervalId = setInterval(() => {
      fetchProducts();
      fetchBasket();
    }, 10000);

    // Clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array ensures this effect runs once on mount and sets up the interval

  // Handle tab changes
  const handleTabChange = (tab) => {
    setActiveTab(tab);
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