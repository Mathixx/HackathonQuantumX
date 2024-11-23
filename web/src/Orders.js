import React, { useState } from "react";

function Orders() {
  const [orders, setOrders] = useState([]);
  
  const handleAddOrders = (product) => {
    setOrders([...orders, product]);
  };
  
  return (
    <div>
      <h3>Basket</h3>
      <ul>
        {orders.map((item, index) => (
          <li key={index}>
            {item.name} - {item.price}
          </li>
        ))}
      </ul>
      <button onClick={() => handleAddOrders({ name: 'Product 1', price: '$10' })}>
        Add Product 1 to Basket
      </button>
    </div>
  );
}

export default Orders;
