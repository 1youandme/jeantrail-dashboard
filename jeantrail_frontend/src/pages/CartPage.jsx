import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function CartPage() {
  const [cartItems, setCartItems] = useState([
    {
      id: 1,
      name: "Portable Blender",
      price: 29.99,
      quantity: 1,
      image_url: "https://example.com/blender.jpg",
    },
    {
      id: 2,
      name: "Triple Laptop Screen",
      price: 149.99,
      quantity: 2,
      image_url: "https://example.com/screen.jpg",
    },
  ]);

  const navigate = useNavigate();
  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2);

  return (
    <motion.div className="max-w-4xl mx-auto py-10 px-6"
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
      <h2 className="text-3xl font-bold mb-6">Your Cart</h2>
      {cartItems.length === 0 ? (
        <p className="text-gray-600">Your cart is empty.</p>
      ) : (
        <>
          <div className="space-y-4">
            {cartItems.map((item) => (
              <div key={item.id} className="flex items-center border rounded p-4">
                <img src={item.image_url} alt={item.name} className="w-24 h-24 object-cover rounded" />
                <div className="ml-4 flex-1">
                  <h3 className="font-semibold">{item.name}</h3>
                  <p className="text-gray-600">${item.price} x {item.quantity}</p>
                </div>
                <p className="font-bold text-primary">${(item.price * item.quantity).toFixed(2)}</p>
              </div>
            ))}
          </div>
          <div className="mt-6 flex justify-between items-center">
            <h4 className="text-xl font-semibold">Total: ${total}</h4>
            <button className="bg-primary text-white px-6 py-2 rounded" onClick={() => navigate("/checkout")}>
              Go to Checkout
            </button>
          </div>
        </>
      )}
    </motion.div>
  );
}
