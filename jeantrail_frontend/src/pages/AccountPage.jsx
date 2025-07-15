import { motion } from "framer-motion";

export default function AccountPage() {
  return (
    <motion.div className="max-w-md mx-auto py-12 px-6"
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
      <h2 className="text-2xl font-bold mb-6">My Account</h2>
      <form className="space-y-4">
        <input className="w-full border p-2 rounded" placeholder="Email" />
        <input className="w-full border p-2 rounded" placeholder="Password" type="password" />
        <button className="bg-primary text-white px-4 py-2 rounded w-full">Login</button>
      </form>
    </motion.div>
  );
}
