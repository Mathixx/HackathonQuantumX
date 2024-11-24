import React from "react";

function Basket({ basket }) {
  return (
    <div>
      <h3>Basket</h3>
      <div className="basket-list">
        {basket.length > 0 ? (
          basket.map((item, index) => (
            <div key={index} className="basket-item">
              <div className="item-info">
                <h4 className="item-name">{item.name}</h4>
                <p className="item-quantity">Qty: {item.quantity}</p>
                <p className="item-price">${item.price}</p>
              </div>
            </div>
          ))
        ) : (
          <p>Your basket is empty.</p>
        )}
      </div>
    </div>
  );
}

export default Basket;
