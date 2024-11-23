import React, { useState, useEffect } from "react";

function ProductList() {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    // Fetch products or update based on chat input
    setProducts([
      { id: 1, name: 'Product 1', price: '$10' },
      { id: 2, name: 'Product 2', price: '$15' },
      { id: 3, name: 'Product 3', price: '$20' },
    ]);
  }, []);
  
  return (
    <div>
      <h3>Products</h3>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            {product.name} - {product.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductList;
