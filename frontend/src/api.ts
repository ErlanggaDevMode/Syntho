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

export interface TransactionInput {
  type: string;
  amount: number;
  category: string;
  description: string;
  payment_method: string;
}

export interface TransactionItem extends TransactionInput {
  id: string;
  transaction_date: string;
}

export interface NoteInput {
  title: string;
  content: string;
  tags: string[];
}

export interface NoteItem extends NoteInput {
  id: string;
  summary: string;
  created_at: string;
}

// Mock LocalStorage database for fallback offline states
const getMockData = <T>(key: string, defaultVal: T): T => {
  const val = localStorage.getItem(key);
  return val ? JSON.parse(val) : defaultVal;
};

const setMockData = <T>(key: string, data: T) => {
  localStorage.setItem(key, JSON.stringify(data));
};

// Seed initial mock data if localStorage is empty
if (!localStorage.getItem('mock_transactions')) {
  setMockData<TransactionItem[]>('mock_transactions', [
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
  setMockData<NoteItem[]>('mock_notes', [
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
  } catch {
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
    throw new Error('Authentication failed');
  }
};

// Transactions CRUD Actions
export const fetchTransactions = async (): Promise<TransactionItem[]> => {
  try {
    const res = await api.get('/transactions');
    return res.data;
  } catch {
    return getMockData<TransactionItem[]>('mock_transactions', []);
  }
};

export const createTransaction = async (data: TransactionInput): Promise<TransactionItem> => {
  try {
    const res = await api.post('/transactions', data);
    return res.data;
  } catch {
    const list = getMockData<TransactionItem[]>('mock_transactions', []);
    const newTx: TransactionItem = { id: Math.random().toString(), ...data, transaction_date: new Date().toISOString() };
    setMockData<TransactionItem[]>('mock_transactions', [newTx, ...list]);
    return newTx;
  }
};

export const deleteTransaction = async (id: string): Promise<void> => {
  try {
    await api.delete(`/transactions/${id}`);
  } catch {
    const list = getMockData<TransactionItem[]>('mock_transactions', []);
    setMockData<TransactionItem[]>('mock_transactions', list.filter((t) => t.id !== id));
  }
};

// Notes CRUD Actions
export const fetchNotes = async (): Promise<NoteItem[]> => {
  try {
    const res = await api.get('/notes');
    return res.data;
  } catch {
    return getMockData<NoteItem[]>('mock_notes', []);
  }
};

export const createNote = async (data: NoteInput): Promise<NoteItem> => {
  try {
    const res = await api.post('/notes', data);
    return res.data;
  } catch {
    const list = getMockData<NoteItem[]>('mock_notes', []);
    const newNote: NoteItem = {
      id: Math.random().toString(),
      created_at: new Date().toISOString(),
      tags: data.tags || ['catatan'],
      summary: data.title + ' summary...',
      ...data,
    };
    setMockData<NoteItem[]>('mock_notes', [newNote, ...list]);
    return newNote;
  }
};

export const deleteNote = async (id: string): Promise<void> => {
  try {
    await api.delete(`/notes/${id}`);
  } catch {
    const list = getMockData<NoteItem[]>('mock_notes', []);
    setMockData<NoteItem[]>('mock_notes', list.filter((n) => n.id !== id));
  }
};
