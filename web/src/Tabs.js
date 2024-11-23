import React from "react";

function Tabs({ activeTab, setActiveTab }) {
  return (
    <div className="tabs">
      <button
        className={activeTab === 'products' ? 'tab active' : 'tab'}
        onClick={() => setActiveTab('products')}
      >
        Products
      </button>
      <button
        className={activeTab === 'basket' ? 'tab active' : 'tab'}
        onClick={() => setActiveTab('basket')}
      >
        Basket
      </button>
      <button
        className={activeTab === 'orders' ? 'tab active' : 'tab'}
        onClick={() => setActiveTab('orders')}
      >
        Orders
      </button>
    </div>
  );
}

export default Tabs;
