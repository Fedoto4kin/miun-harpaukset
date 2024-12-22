// src/axios.js
import axios from 'axios';

const baseURL = process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : '/api';

const axiosInstance = axios.create({
  baseURL: baseURL,
});

export default axiosInstance;
