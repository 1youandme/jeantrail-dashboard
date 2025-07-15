import { motion } from "framer-motion";

export default function CheckoutPage() {
  return (
    <motion.div className="max-w-2xl mx-auto py-10 px-6"
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
      <h2 className="text-2xl font-bold mb-6">Checkout</h2>
      <form className="space-y-4">
        <input className="w-full border p-2 rounded" placeholder="Full Name" />
        <input className="w-full border p-2 rounded" placeholder="Email" />
        <input className="w-full border p-2 rounded" placeholder="Shipping Address" />
        <select className="w-full border p-2 rounded">
          <option>Visa / Mastercard</option>
          <option>PayPal</option>
          <option>Fawry</option>
          <option>Instapay</option>
        </select>
        <button className="bg-primary text-white px-4 py-2 rounded">Pay Now</button>
      </form>
    </motion.div>
  );
}
