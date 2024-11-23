import React, { useState, useEffect } from "react";

function ProductList({ updateTrigger }) {
  const [products, setProducts] = useState([]);

  // Fetch products whenever updateTrigger changes
  useEffect(() => {
    const fetchUpdatedProducts = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get-products", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (response.ok) {
          const data = await response.json();
          setProducts(data.products);
        } else {
          console.error("Failed to fetch products:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    // Fetch products if the updateTrigger is true
    if (updateTrigger) {
      fetchUpdatedProducts(); 
    }

  }, [updateTrigger]); // Dependency on updateTrigger

  return (
    <div>
      <h3>Products</h3>
      <ul>
        {products.length > 0 ? (
          products.map((product) => (
            <li key={product.id}>
              {product.name} - {product.price}
            </li>
          ))
        ) : (
          <li>No products available.</li>
        )}
      </ul>
    </div>
  );
}

export default ProductList;
