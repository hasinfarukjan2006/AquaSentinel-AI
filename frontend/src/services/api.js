import axios from 'axios';

const RAW_BASE = (import.meta.env.VITE_API_BASE_URL || 'https://aquasentinel-ai-4mlr.onrender.com').replace(/\/+$/, '');
const API_BASE = RAW_BASE ? (RAW_BASE.endsWith('/api') ? RAW_BASE : `${RAW_BASE}/api`) : '/api';

export const fetchHealth = async () => {
  const res = await axios.get(`${API_BASE}/health`);
  return res.data;
};

export const fetchSummary = async (dataType = 'REAL_PUBLIC_SOURCE') => {
  const res = await axios.get(`${API_BASE}/summary?data_type=${dataType}`);
  return res.data;
};

export const fetchLocations = async (dataType = 'REAL_PUBLIC_SOURCE') => {
  const res = await axios.get(`${API_BASE}/locations?data_type=${dataType}`);
  return res.data;
};

export const fetchRiskRecords = async (dataType = 'REAL_PUBLIC_SOURCE', params = {}) => {
  const query = new URLSearchParams({ data_type: dataType, ...params }).toString();
  const res = await axios.get(`${API_BASE}/risk-monitoring?${query}`);
  return res.data;
};

export const fetchLocationRisk = async (location, dataType = 'REAL_PUBLIC_SOURCE') => {
  const res = await axios.get(`${API_BASE}/risk/${encodeURIComponent(location)}?data_type=${dataType}`);
  return res.data;
};

export const fetchWaterQuality = async (dataType = 'REAL_PUBLIC_SOURCE', district = '') => {
  const query = new URLSearchParams({ data_type: dataType, district }).toString();
  const res = await axios.get(`${API_BASE}/water-quality?${query}`);
  return res.data;
};

export const fetchRainfall = async (dataType = 'REAL_PUBLIC_SOURCE') => {
  const res = await axios.get(`${API_BASE}/rainfall?data_type=${dataType}`);
  return res.data;
};

export const fetchHealthData = async (dataType = 'REAL_PUBLIC_SOURCE') => {
  const res = await axios.get(`${API_BASE}/health-incidents?data_type=${dataType}`);
  return res.data;
};

export const fetchDataExplorer = async (dataType = 'REAL_PUBLIC_SOURCE', params = {}) => {
  const query = new URLSearchParams({ data_type: dataType, ...params }).toString();
  const res = await axios.get(`${API_BASE}/data-explorer?${query}`);
  return res.data;
};

export const fetchDataStatus = async () => {
  const res = await axios.get(`${API_BASE}/data-status`);
  return res.data;
};

export const fetchAlerts = async (dataType = 'REAL_PUBLIC_SOURCE', level = '') => {
  const query = new URLSearchParams({ data_type: dataType, level }).toString();
  const res = await axios.get(`${API_BASE}/alerts?${query}`);
  return res.data;
};

export const fetchModelStatus = async () => {
  const res = await axios.get(`${API_BASE}/model/status`);
  return res.data;
};

export const fetchDataQuality = async () => {
  const res = await axios.get(`${API_BASE}/data-quality`);
  return res.data;
};

export const predictRisk = async (recordData) => {
  const res = await axios.post(`${API_BASE}/risk/predict`, recordData);
  return res.data;
};
