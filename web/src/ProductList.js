import React from "react";

function ProductList({ products }) {
  return (
    <div>
      <h3>Products</h3>
      <div className="product-list">
        {products.length > 0 ? (
          products.map((product, index) => (
            <div key={index} className="product-card">
              <h4 className="product-name">{product.name}</h4>
              <p className="product-price">${product.price}</p>
            </div>
          ))
        ) : (
          <p>No products available.</p>
        )}
      </div>
    </div>
  );
}

export default ProductList;
