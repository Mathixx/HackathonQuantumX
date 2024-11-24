import React from "react";

function ProductList({ products }) {
  return (
    <div>
      <h3>Products</h3>
      <ul>
        {products.length > 0 ? (
          products.map((product, index) => (
            <li key={index}>
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