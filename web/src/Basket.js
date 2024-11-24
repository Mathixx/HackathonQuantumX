import React from "react";

function Basket({ basket }) {
  return (
    <div>
      <h3>Basket</h3>
      <ul>
        {basket.length > 0 ? (
          basket.map((item, index) => (
            <li key={index}>
              {item.name} - Quantity: {item.quantity} - Price: {item.price}
            </li>
          ))
        ) : (
          <li>Your basket is empty.</li>
        )}
      </ul>
    </div>
  );
}

export default Basket;

