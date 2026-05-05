import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL
  || (window.location.hostname === 'localhost'
    ? 'http://localhost:3001'
    : 'https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com');

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
});

// ── Shared endpoints (not model-specific) ──
export const getAvailableDates = async () => {
  const res = await api.get('/races/available-dates');
  return res.data;
};

export const getHorsePPs = async (horseId: string) => {
  const res = await api.get(`/horses/${horseId}/pps`);
  return res.data;
};

export const getDashboardMetrics = async () => {
  const res = await api.get('/dashboard/metrics');
  return res.data;
};

// ── WR Model API ──
export const getWRRacesToday = async () => {
  const res = await api.get('/races/today');
  return res.data;
};

export const getWRRacesByDate = async (date: string, style?: string) => {
  // style: 'general' (default omitted) | 'gonzo_sauce' | other gallery styles.
  // Backend defaults to general when omitted; we omit explicitly to keep
  // analytics on the existing endpoint URL pattern unchanged.
  const params = style && style !== 'general' ? { style } : {};
  const res = await api.get(`/races/${date}`, { params });
  return res.data;
};

export const getWRPredictionsToday = async () => {
  const res = await api.get('/wr/predictions/today');
  return res.data;
};

export const getWRValuePlays = async (date?: string) => {
  const params = date ? { date } : {};
  const res = await api.get('/wr/predictions/value', { params });
  return res.data;
};

export const runWRPredictions = async (date: string) => {
  const res = await api.get(`/wr/predictions/run?date=${date}`);
  return res.data;
};

export const getCompareView = async (date: string, style: string) => {
  const res = await api.get(`/wr/predictions/${date}/compare`, {
    params: { style },
  });
  return res.data;
};

// ── P&L Model API ──
export const getPLPredictionsToday = async () => {
  const res = await api.get('/pl/predictions/today');
  return res.data;
};

export const getPLPredictionsByDate = async (date: string) => {
  const res = await api.get(`/pl/predictions/${date}`);
  return res.data;
};

export const getPLValueBets = async (date?: string) => {
  const params = date ? { date } : {};
  const res = await api.get('/pl/predictions/value-bets', { params });
  return res.data;
};

export const runPLPredictions = async (date: string) => {
  const res = await api.get(`/pl/predictions/run?date=${date}`);
  return res.data;
};

// ── LS Model API ──
export const getLSPredictionsToday = async () => {
  const res = await api.get('/ls/predictions/today');
  return res.data;
};

export const getLSPredictionsByDate = async (date: string) => {
  const res = await api.get(`/ls/predictions/${date}`);
  return res.data;
};

export const getLSAlerts = async (date?: string) => {
  const params = date ? { date } : {};
  const res = await api.get('/ls/predictions/longshots', { params });
  return res.data;
};

export const runLSPredictions = async (date: string) => {
  const res = await api.get(`/ls/predictions/run?date=${date}`);
  return res.data;
};

// ── Legacy aliases — keep BetBuilderPage / HistoryPage working ──
export const getRacesToday = getWRRacesToday;
export const getRacesByDate = getWRRacesByDate;
export const getValuePlays = getWRValuePlays;
export const runPredictions = runWRPredictions;

// ── Stream E4: track-record aggregate banners ──
export const getTrackRecord = async (
  model: 'wr' | 'pl' | 'ls', days: number,
) => {
  const res = await api.get(`/${model}/predictions/track-record?days=${days}`);
  return res.data;
};

export const getTrackRecordByStyle = async (days: number) => {
  const res = await api.get(`/wr/predictions/track-record-by-style?days=${days}`);
  return res.data;
};

export default api;
