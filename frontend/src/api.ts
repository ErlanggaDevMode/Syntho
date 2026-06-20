import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach Authorization Bearer token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('syntho_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Mock LocalStorage database for fallback offline states
const getMockData = (key: string, defaultVal: any) => {
  const val = localStorage.getItem(key);
  return val ? JSON.parse(val) : defaultVal;
};

const setMockData = (key: string, data: any) => {
  localStorage.setItem(key, JSON.stringify(data));
};

// Seed initial mock data if localStorage is empty
if (!localStorage.getItem('mock_transactions')) {
  setMockData('mock_transactions', [
    {
      id: '1',
      type: 'expense',
      amount: 25000,
      category: 'Makanan',
      description: 'Makan siang di warteg',
      payment_method: 'Tunai',
      transaction_date: new Date(Date.now() - 3600000 * 2).toISOString(),
    },
    {
      id: '2',
      type: 'expense',
      amount: 50000,
      category: 'Transportasi',
      description: 'Beli bensin',
      payment_method: 'QRIS',
      transaction_date: new Date(Date.now() - 3600000 * 12).toISOString(),
    },
    {
      id: '3',
      type: 'income',
      amount: 3000000,
      category: 'Gaji',
      description: 'Gaji Bulanan',
      payment_method: 'Transfer',
      transaction_date: new Date(Date.now() - 3600000 * 24 * 3).toISOString(),
    },
    {
      id: '4',
      type: 'expense',
      amount: 15000,
      category: 'Kopi',
      description: 'Es kopi susu',
      payment_method: 'QRIS',
      transaction_date: new Date(Date.now() - 3600000 * 24 * 5).toISOString(),
    },
  ]);
}

if (!localStorage.getItem('mock_notes')) {
  setMockData('mock_notes', [
    {
      id: '1',
      title: 'Ide Konten Finansial',
      content: 'Membuat konten edukasi tentang penghematan harian menggunakan metode budgeting 50-30-20.',
      summary: 'Edukasi cara budgeting harian.',
      tags: ['edukasi', 'budgeting', 'finansial'],
      created_at: new Date(Date.now() - 3600000 * 24 * 2).toISOString(),
    },
    {
      id: '2',
      title: 'Rencana Belanja Bulanan',
      content: 'Beli beras 5kg, minyak goreng 2L, telur 1kg, sabun mandi, deterjen cair.',
      summary: 'Daftar belanja bulanan pokok.',
      tags: ['belanja', 'pokok'],
      created_at: new Date().toISOString(),
    },
  ]);
}

// User Profile Actions
export const fetchUserProfile = async () => {
  try {
    const res = await api.get('/auth/me');
    return res.data;
  } catch (err) {
    // Fallback if backend is offline
    const token = localStorage.getItem('syntho_token');
    if (token) {
      return {
        id: 'mock-user-uuid',
        telegram_id: 123456789,
        username: 'johndoe',
        full_name: 'John Doe',
        timezone: 'Asia/Jakarta',
        created_at: new Date().toISOString(),
      };
    }
    throw err;
  }
};

// Transactions CRUD Actions
export const fetchTransactions = async () => {
  try {
    const res = await api.get('/transactions');
    return res.data;
  } catch (err) {
    return getMockData('mock_transactions', []);
  }
};

export const createTransaction = async (data: any) => {
  try {
    const res = await api.post('/transactions', data);
    return res.data;
  } catch (err) {
    const list = getMockData('mock_transactions', []);
    const newTx = { id: Math.random().toString(), ...data, transaction_date: new Date().toISOString() };
    setMockData('mock_transactions', [newTx, ...list]);
    return newTx;
  }
};

export const deleteTransaction = async (id: string) => {
  try {
    await api.delete(`/transactions/${id}`);
  } catch (err) {
    const list = getMockData('mock_transactions', []);
    setMockData('mock_transactions', list.filter((t: any) => t.id !== id));
  }
};

// Notes CRUD Actions
export const fetchNotes = async () => {
  try {
    const res = await api.get('/notes');
    return res.data;
  } catch (err) {
    return getMockData('mock_notes', []);
  }
};

export const createNote = async (data: any) => {
  try {
    const res = await api.post('/notes', data);
    return res.data;
  } catch (err) {
    const list = getMockData('mock_notes', []);
    const newNote = {
      id: Math.random().toString(),
      created_at: new Date().toISOString(),
      tags: data.tags || ['catatan'],
      summary: data.summary || data.content.slice(0, 50) + '...',
      ...data,
    };
    setMockData('mock_notes', [newNote, ...list]);
    return newNote;
  }
};

export const deleteNote = async (id: string) => {
  try {
    await api.delete(`/notes/${id}`);
  } catch (err) {
    const list = getMockData('mock_notes', []);
    setMockData('mock_notes', list.filter((n: any) => n.id !== id));
  }
};
