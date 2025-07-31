// src/context/AuthContext.jsx
import React, { createContext, useContext, useEffect, useState } from "react";
import api from "../api/axios"; // custom axios instance

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // Login function
  const login = async (email, password) => {
    const res = await api.post("/auth/login", { email, password });

    if (!res || !res.data) {
      throw new Error("Login failed");
    }

    setUser(res.data.user);
    console.log("User logged in:", res.data);
    setToken(res.data.access_token);
    localStorage.setItem("token", res.data.access_token);
  };

  const logout = async () => {
    await api.post("/auth/logout");
    setUser(null);
    setToken(null);
  };

  // Attach auth headers to api instance
  useEffect(() => {
    if (token) {
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      delete api.defaults.headers.common["Authorization"];
    }
  }, [token]);

  // Auto login if session exists
  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await api.get("/auth/me");
        if (res.data) {
          setUser(res.data.user);
          if (res.data.access_token) {
            setToken(res.data.access_token);
          }
        }
      } catch (err) {
        console.error("No active session");
      }
    };
    checkSession();
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
