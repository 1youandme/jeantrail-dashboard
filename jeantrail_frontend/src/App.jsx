import ShopPage from "./pages/ShopPage";
import { useEffect, useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Menu } from "lucide-react";
import axios from "axios";

// ======================== Header ==========================
function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [backendMessage, setBackendMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/ping')
      .then((res) => setBackendMessage(res.data.message))
      .catch((err) => console.error("Error fetching from backend:", err));
  }, []);

  return (
    <header className="w-full bg-white shadow-md py-4 px-6 flex justify-between items-center relative">
      <div className="text-2xl font-bold text-primary">JeanTrail</div>
      <nav className="space-x-6 hidden md:flex">
        <Link to="/">Home</Link>
        <Link to="/shop">Shop</Link>
        <Link to="/contact">Contact</Link>
        <Link to="/account">My Account</Link>
        <Link to="/cart">Cart</Link>
      </nav>
      <div className="md:hidden flex items-center gap-4">
        <button onClick={() => setMenuOpen(!menuOpen)}>
          <Menu className="w-6 h-6 text-gray-700" />
        </button>
        <Link to="/cart">🛒</Link>
      </div>
      {menuOpen && (
        <div className="absolute top-16 right-6 bg-white shadow-lg rounded-lg w-40 py-2 px-4 flex flex-col space-y-2 md:hidden z-50">
          <Link to="/" onClick={() => setMenuOpen(false)}>Home</Link>
          <Link to="/shop" onClick={() => setMenuOpen(false)}>Shop</Link>
          <Link to="/contact" onClick={() => setMenuOpen(false)}>Contact</Link>
          <Link to="/account" onClick={() => setMenuOpen(false)}>My Account</Link>
          <Link to="/cart" onClick={() => setMenuOpen(false)}>Cart</Link>
        </div>
      )}
      <p className="text-sm text-gray-500 absolute bottom-[-1.5rem] right-4">
        📡 {backendMessage}
      </p>
    </header>
  );
}

// ======================== صفحات ==========================
function NotFoundPage() {
  return (
    <motion.section className="min-h-screen flex items-center justify-center text-center px-6"
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
      <div className="space-y-4">
        <h1 className="text-5xl font-bold text-primary">404</h1>
        <p className="text-gray-600 text-lg">Oops! Page not found.</p>
        <Link to="/"><button>Go Home</button></Link>
      </div>
    </motion.section>
  );
}

function HeroSection() {
  return (
    <section className="flex flex-col items-center justify-center py-20 text-center">
      <h1 className="text-5xl font-bold mb-4">Welcome to JeanTrail</h1>
      <p className="text-gray-600 mb-8">Explore smart & trending products</p>
      <Link to="/shop"><button>Start Shopping</button></Link>
    </section>
  );
}

function HomePage() {
  return <HeroSection />;
}

// ======================== التطبيق الرئيسي ==========================
export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/shop" element={<ShopPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
}
