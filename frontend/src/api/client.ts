import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL
  || 'http://localhost:3001';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
});

export const getRacesToday = async () => {
  const res = await api.get('/races/today');
  return res.data;
};

export const getRacesByDate = async (
  date: string
) => {
  const res = await api.get(`/races/${date}`);
  return res.data;
};

export const getPredictionsToday = async () => {
  const res = await api.get('/predictions/today');
  return res.data;
};

export const getValuePlays = async (
  date?: string
) => {
  const params = date ? { date } : {};
  const res = await api.get(
    '/predictions/value',
    { params }
  );
  return res.data;
};

export const getHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export default api;
