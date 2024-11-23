import React, { useState } from "react";

function Basket() {
  const [basket, setBasket] = useState([]);
  
  const handleAddToBasket = (product) => {
    setBasket([...basket, product]);
  };
  
  return (
    <div>
      <h3>Basket</h3>
      <ul>
        {basket.map((item, index) => (
          <li key={index}>
            {item.name} - {item.price}
          </li>
        ))}
      </ul>
      <button onClick={() => handleAddToBasket({ name: 'Product 1', price: '$10' })}>
        Add Product 1 to Basket
      </button>
    </div>
  );
}

export default Basket;
