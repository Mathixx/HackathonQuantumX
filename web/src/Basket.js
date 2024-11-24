import React, { useState, useEffect } from "react";

function Basket({ updateTrigger }) {
  const [basket, setBasket] = useState([]);

  // Fetch cart contents whenever updateTrigger changes
  useEffect(() => {
    const fetchCart = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get-cart", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (response.ok) {
          const data = await response.json();
          setBasket(data.cart); // Update the basket with the fetched data
        } else {
          console.error("Failed to fetch cart:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching cart:", error);
      }
    };

    fetchCart();
  }, [updateTrigger]); // Re-fetch the cart whenever updateTrigger changes

  // // Function to add a product to the basket (client-side only for now)
  // const handleAddToBasket = async (product) => {
  //   try {
  //     // Update the basket client-side
  //     const updatedBasket = [...basket, product];
  //     setBasket(updatedBasket);

  //     // Optionally, make a POST request to update the server-side cart
  //     const response = await fetch("http://127.0.0.1:5000/add-to-cart", {
  //       method: "POST",
  //       headers: { "Content-Type": "application/json" },
  //       body: JSON.stringify(product),
  //     });

  //     if (!response.ok) {
  //       console.error("Failed to add product to basket:", response.statusText);
  //     }
  //   } catch (error) {
  //     console.error("Error adding product to basket:", error);
  //   }
  // };

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
      {/* Example button for adding a product */}
      {/* <button
        onClick={() => handleAddToBasket({ name: "Product 1", price: 10, quantity: 1 })}
      >
        Add Product 1 to Basket
      </button> */}
    </div>
  );
}

export default Basket;
