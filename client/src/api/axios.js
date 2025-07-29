// api/axios.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api', // Your Flask server with /api prefix
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Don't set Content-Type for FormData requests - let axios handle it
api.interceptors.request.use((config) => {
  // Remove Content-Type header for FormData to let browser set it with boundary
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  return config;
});

export default api;