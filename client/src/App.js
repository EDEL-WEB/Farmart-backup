import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AdminPage from "./pages/AdminPage";
import FarmerPage from "./pages/FarmerPage";
import BuyerPage from "./pages/BuyerPage";
import AnimalList from "./pages/AnimalList";
import AnimalDetailsPage from "./pages/AnimalDetailsPage";
import CartPage from "./pages/CartPage";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/animals" element={<AnimalList />} />
        <Route path="/animals/:id" element={<AnimalDetailsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={["admin"]} element={<AdminPage />} />
          }
        />
        <Route
          path="/farmer"
          element={
            <ProtectedRoute allowedRoles={["farmer"]} element={<FarmerPage />} />
          }
        />
        <Route
          path="/buyer"
          element={
            <ProtectedRoute allowedRoles={["buyer"]} element={<BuyerPage />} />
          }
        />
        <Route
          path="/cart"
          element={
            <ProtectedRoute allowedRoles={["buyer"]} element={<CartPage />} />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
