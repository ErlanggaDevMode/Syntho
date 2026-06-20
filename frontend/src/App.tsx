import { useState } from 'react';
import { 
  QueryClient, 
  QueryClientProvider, 
  useQuery, 
  useMutation, 
  useQueryClient 
} from '@tanstack/react-query';
import { 
  LayoutDashboard, 
  Receipt, 
  FileText, 
  TrendingUp, 
  Settings as SettingsIcon, 
  LogOut, 
  Plus, 
  Search, 
  Filter, 
  Moon, 
  Sun, 
  Download, 
  Trash2, 
  Key, 
  CheckCircle,
  Clock,
  Tag
} from 'lucide-react';
import { 
  fetchUserProfile, 
  fetchTransactions, 
  createTransaction, 
  deleteTransaction, 
  fetchNotes, 
  createNote, 
  deleteNote 
} from './api';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function DashboardContent() {
  const [activeTab, setActiveTab] = useState<'overview' | 'transactions' | 'notes' | 'reports' | 'settings'>('overview');
  const [darkMode, setDarkMode] = useState(true);
  const [token, setToken] = useState<string | null>(localStorage.getItem('syntho_token'));

  // Modals state
  const [showTxModal, setShowTxModal] = useState(false);
  const [showNoteModal, setShowNoteModal] = useState(false);

  // Form states
  const [txForm, setTxForm] = useState({ type: 'expense', amount: '', category: 'Makanan', description: '', payment_method: 'QRIS' });
  const [noteForm, setNoteForm] = useState({ title: '', content: '', tagsString: '' });

  // Query state hooks
  const queryClientObj = useQueryClient();

  const { data: user } = useQuery({
    queryKey: ['user', token],
    queryFn: fetchUserProfile,
    enabled: !!token,
  });

  const { data: transactions = [] } = useQuery({
    queryKey: ['transactions', token],
    queryFn: fetchTransactions,
    enabled: !!token,
  });

  const { data: notes = [] } = useQuery({
    queryKey: ['notes', token],
    queryFn: fetchNotes,
    enabled: !!token,
  });

  // Mutations
  const addTxMutation = useMutation({
    mutationFn: createTransaction,
    onSuccess: () => {
      queryClientObj.invalidateQueries({ queryKey: ['transactions'] });
      setShowTxModal(false);
      setTxForm({ type: 'expense', amount: '', category: 'Makanan', description: '', payment_method: 'QRIS' });
    },
  });

  const removeTxMutation = useMutation({
    mutationFn: deleteTransaction,
    onSuccess: () => {
      queryClientObj.invalidateQueries({ queryKey: ['transactions'] });
    },
  });

  const addNoteMutation = useMutation({
    mutationFn: createNote,
    onSuccess: () => {
      queryClientObj.invalidateQueries({ queryKey: ['notes'] });
      setShowNoteModal(false);
      setNoteForm({ title: '', content: '', tagsString: '' });
    },
  });

  const removeNoteMutation = useMutation({
    mutationFn: deleteNote,
    onSuccess: () => {
      queryClientObj.invalidateQueries({ queryKey: ['notes'] });
    },
  });

  // Transaction Filters
  const [txSearch, setTxSearch] = useState('');
  const [txTypeFilter, setTxTypeFilter] = useState('all');
  const [txCategoryFilter, setTxCategoryFilter] = useState('all');
  const [txPage, setTxPage] = useState(1);
  const txPerPage = 5;

  // Notes Filters
  const [noteSearch, setNoteSearch] = useState('');

  // Handle Mock Login Simulation
  const handleSimulateLogin = () => {
    // Generate a mock JWT token and store it
    const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb2NrLXVzZXItdXVpZCJ9.signature';
    localStorage.setItem('syntho_token', mockToken);
    setToken(mockToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('syntho_token');
    setToken(null);
    setActiveTab('overview');
  };

  // Helper metrics calculation
  const totalIncome = transactions
    .filter((t: any) => t.type === 'income')
    .reduce((sum: number, t: any) => sum + Number(t.amount), 0);

  const totalExpense = transactions
    .filter((t: any) => t.type === 'expense')
    .reduce((sum: number, t: any) => sum + Number(t.amount), 0);

  const netBalance = totalIncome - totalExpense;

  // Filtered lists
  const filteredTxs = transactions.filter((t: any) => {
    const matchesSearch = t.description?.toLowerCase().includes(txSearch.toLowerCase()) || 
                          t.category?.toLowerCase().includes(txSearch.toLowerCase());
    const matchesType = txTypeFilter === 'all' || t.type === txTypeFilter;
    const matchesCategory = txCategoryFilter === 'all' || t.category === txCategoryFilter;
    return matchesSearch && matchesType && matchesCategory;
  });

  const paginatedTxs = filteredTxs.slice((txPage - 1) * txPerPage, txPage * txPerPage);
  const totalTxPages = Math.ceil(filteredTxs.length / txPerPage) || 1;

  const filteredNotes = notes.filter((n: any) => {
    return n.title?.toLowerCase().includes(noteSearch.toLowerCase()) || 
           n.content?.toLowerCase().includes(noteSearch.toLowerCase()) ||
           n.tags?.some((tag: string) => tag.toLowerCase().includes(noteSearch.toLowerCase()));
  });

  // Export report handler
  const handleExportCSV = () => {
    const headers = 'ID,Tanggal,Tipe,Nominal,Kategori,Deskripsi,Metode Pembayaran\n';
    const rows = transactions.map((t: any) => 
      `"${t.id}","${t.transaction_date}","${t.type}",${t.amount},"${t.category}","${t.description}","${t.payment_method}"`
    ).join('\n');
    const blob = new Blob([headers + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `syntho_report_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Render Login state if not authenticated
  if (!token) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden font-sans">
        {/* Futuristic glowing backdrops */}
        <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] rounded-full bg-purple-900/10 blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] rounded-full bg-blue-900/10 blur-[120px] pointer-events-none" />

        <div className="sm:mx-auto sm:w-full sm:max-w-md text-center z-10">
          <div className="mx-auto h-16 w-16 bg-gradient-to-tr from-purple-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-xl shadow-purple-500/20 border border-purple-500/30">
            <LayoutDashboard className="h-9 w-9 text-white" />
          </div>
          <h2 className="mt-6 text-center text-4xl font-extrabold tracking-tight text-white font-sans">
            Syntho
          </h2>
          <p className="mt-2 text-center text-sm text-slate-400">
            Self-hosted AI-powered Notes & Expense Assistant
          </p>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md z-10 px-4 sm:px-0">
          <div className="bg-slate-900/50 backdrop-blur-xl py-8 px-4 shadow-2xl rounded-2xl sm:px-10 border border-slate-800/80">
            <div className="space-y-6">
              <div className="text-center">
                <p className="text-slate-300 text-sm mb-4">
                  Syntho terintegrasi secara privat dengan Telegram Bot Anda.
                </p>
                <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800 text-left text-xs space-y-2 text-slate-400">
                  <div className="flex items-center text-slate-300 font-semibold gap-1.5">
                    <Key className="h-3.5 w-3.5 text-purple-400" />
                    <span>Langkah Login:</span>
                  </div>
                  <p>1. Rekam transaksi/catatan Anda via Bot Telegram.</p>
                  <p>2. Login di web ini menggunakan Telegram Login Widget.</p>
                </div>
              </div>

              <div>
                <button
                  type="button"
                  onClick={handleSimulateLogin}
                  className="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-md text-sm font-semibold text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-all cursor-pointer"
                >
                  Masuk dengan Telegram (Simulasi)
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen flex ${darkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'} transition-all duration-300 font-sans`}>
      {/* Sidebar navigation */}
      <aside className={`w-64 border-r ${darkMode ? 'bg-slate-900/60 border-slate-800/80' : 'bg-white border-slate-200'} flex flex-col justify-between p-6 z-10 backdrop-blur-lg`}>
        <div className="space-y-8">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 bg-gradient-to-tr from-purple-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/10 border border-purple-500/20">
              <LayoutDashboard className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg tracking-tight">Syntho</h1>
              <span className="text-xs text-purple-400 font-medium">Self-hosted</span>
            </div>
          </div>

          <nav className="space-y-1">
            {[
              { id: 'overview', label: 'Overview', icon: LayoutDashboard },
              { id: 'transactions', label: 'Transaksi', icon: Receipt },
              { id: 'notes', label: 'Catatan', icon: FileText },
              { id: 'reports', label: 'Laporan', icon: TrendingUp },
              { id: 'settings', label: 'Pengaturan', icon: SettingsIcon },
            ].map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id as any)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all cursor-pointer ${
                    isActive 
                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/20' 
                      : darkMode ? 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                  }`}
                >
                  <Icon className="h-4.5 w-4.5" />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between px-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Tema</span>
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className={`p-2 rounded-xl border ${darkMode ? 'border-slate-800 bg-slate-950/40 text-yellow-400 hover:bg-slate-800' : 'border-slate-200 bg-slate-100 text-slate-700 hover:bg-slate-200'} cursor-pointer`}
            >
              {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
          </div>

          <div className={`p-4 rounded-2xl border ${darkMode ? 'bg-slate-950/40 border-slate-800/80' : 'bg-slate-50 border-slate-200'} flex items-center gap-3`}>
            <div className="h-10 w-10 rounded-full bg-purple-500/10 flex items-center justify-center font-bold text-purple-400 border border-purple-500/20">
              {user?.full_name?.slice(0, 2).toUpperCase() || 'US'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold truncate">{user?.full_name || 'Loading...'}</p>
              <p className="text-xs text-slate-500 truncate">@{user?.username || 'user'}</p>
            </div>
            <button 
              onClick={handleLogout}
              className="p-1.5 text-slate-500 hover:text-red-400 transition-colors cursor-pointer"
              title="Logout"
            >
              <LogOut className="h-4.5 w-4.5" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-10 overflow-y-auto max-w-7xl mx-auto w-full relative">
        {/* Glow dots */}
        <div className="absolute top-0 right-1/4 w-[400px] h-[400px] rounded-full bg-purple-500/5 blur-[100px] pointer-events-none" />

        {/* Tab components display */}
        {activeTab === 'overview' && (
          <div className="space-y-8 animate-fade-in">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-3xl font-extrabold tracking-tight">Overview</h2>
                <p className="text-sm text-slate-500">Pantau keuangan dan catatan terintegrasi Anda.</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setShowTxModal(true)}
                  className="flex items-center gap-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white text-sm font-semibold rounded-xl shadow-lg shadow-purple-500/10 cursor-pointer"
                >
                  <Plus className="h-4 w-4" />
                  Tambah Transaksi
                </button>
                <button
                  onClick={() => setShowNoteModal(true)}
                  className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 active:bg-slate-900 border border-slate-700/80 text-white text-sm font-semibold rounded-xl cursor-pointer"
                >
                  <Plus className="h-4 w-4" />
                  Catatan Baru
                </button>
              </div>
            </div>

            {/* Financial metric summaries */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200 shadow-sm'}`}>
                <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Saldo Bersih</p>
                <p className={`text-3xl font-black mt-2 ${netBalance >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  Rp {netBalance.toLocaleString('id-ID')}
                </p>
                <p className="text-xs text-slate-500 mt-1">Selisih pemasukan - pengeluaran</p>
              </div>
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200 shadow-sm'}`}>
                <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Total Pemasukan</p>
                <p className="text-3xl font-black mt-2 text-emerald-400">
                  Rp {totalIncome.toLocaleString('id-ID')}
                </p>
                <p className="text-xs text-slate-500 mt-1">Berdasarkan total transaksi masuk</p>
              </div>
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200 shadow-sm'}`}>
                <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Total Pengeluaran</p>
                <p className="text-3xl font-black mt-2 text-rose-400">
                  Rp {totalExpense.toLocaleString('id-ID')}
                </p>
                <p className="text-xs text-slate-500 mt-1">Berdasarkan total transaksi keluar</p>
              </div>
            </div>

            {/* Recent Items Lists */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Recent Transactions list */}
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200 shadow-sm'} space-y-4`}>
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-lg">Transaksi Terbaru</h3>
                  <button onClick={() => setActiveTab('transactions')} className="text-xs text-purple-400 font-semibold hover:underline cursor-pointer">Lihat Semua</button>
                </div>
                {transactions.length === 0 ? (
                  <p className="text-sm text-slate-500 py-6 text-center">Belum ada transaksi terekam.</p>
                ) : (
                  <div className="divide-y divide-slate-800/60 space-y-3">
                    {transactions.slice(0, 4).map((t: any) => (
                      <div key={t.id} className="flex items-center justify-between pt-3 first:pt-0">
                        <div className="min-w-0">
                          <p className="text-sm font-bold truncate">{t.description || 'Tanpa deskripsi'}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${t.type === 'income' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
                              {t.type === 'income' ? 'Pemasukan' : 'Pengeluaran'}
                            </span>
                            <span className="text-xs text-slate-500">{t.category}</span>
                          </div>
                        </div>
                        <p className={`text-sm font-black ${t.type === 'income' ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {t.type === 'income' ? '+' : '-'} Rp {Number(t.amount).toLocaleString('id-ID')}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Recent Notes grid */}
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200 shadow-sm'} space-y-4`}>
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-lg">Catatan Terbaru</h3>
                  <button onClick={() => setActiveTab('notes')} className="text-xs text-purple-400 font-semibold hover:underline cursor-pointer">Lihat Semua</button>
                </div>
                {notes.length === 0 ? (
                  <p className="text-sm text-slate-500 py-6 text-center">Belum ada catatan disimpan.</p>
                ) : (
                  <div className="grid grid-cols-1 gap-4">
                    {notes.slice(0, 2).map((n: any) => (
                      <div key={n.id} className={`p-4 rounded-xl border ${darkMode ? 'bg-slate-950/60 border-slate-800/60' : 'bg-slate-50 border-slate-200'} space-y-2`}>
                        <h4 className="font-bold text-sm text-purple-400">{n.title}</h4>
                        <p className="text-xs text-slate-400 line-clamp-2">{n.content}</p>
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {n.tags?.map((tag: string) => (
                            <span key={tag} className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded-md flex items-center gap-0.5">
                              <Tag className="h-2.5 w-2.5 text-slate-500" />
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Transactions Tab components view */}
        {activeTab === 'transactions' && (
          <div className="space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-extrabold tracking-tight">Daftar Transaksi</h2>
                <p className="text-sm text-slate-500">Kelola riwayat pengeluaran dan pemasukan Anda.</p>
              </div>
              <button
                onClick={() => setShowTxModal(true)}
                className="flex items-center gap-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white text-sm font-semibold rounded-xl cursor-pointer"
              >
                <Plus className="h-4 w-4" />
                Tambah Transaksi
              </button>
            </div>

            {/* Filters panel */}
            <div className={`p-4 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200'} flex flex-col md:flex-row md:items-center justify-between gap-4`}>
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                <input
                  type="text"
                  placeholder="Cari deskripsi atau kategori..."
                  value={txSearch}
                  onChange={(e) => { setTxSearch(e.target.value); setTxPage(1); }}
                  className={`w-full pl-9 pr-4 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <Filter className="h-4 w-4 text-slate-500" />
                  <select
                    value={txTypeFilter}
                    onChange={(e) => { setTxTypeFilter(e.target.value); setTxPage(1); }}
                    className={`px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                      darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                    }`}
                  >
                    <option value="all">Semua Tipe</option>
                    <option value="expense">Pengeluaran</option>
                    <option value="income">Pemasukan</option>
                  </select>
                </div>

                <select
                  value={txCategoryFilter}
                  onChange={(e) => { setTxCategoryFilter(e.target.value); setTxPage(1); }}
                  className={`px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                >
                  <option value="all">Semua Kategori</option>
                  {Array.from(new Set(transactions.map((t: any) => t.category))).filter(Boolean).map((cat: any) => (
                    <option key={String(cat)} value={String(cat)}>{String(cat)}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Table display */}
            <div className={`border rounded-2xl overflow-hidden ${darkMode ? 'bg-slate-900/20 border-slate-800/80' : 'bg-white border-slate-200 shadow-sm'}`}>
              <table className="min-w-full divide-y divide-slate-800/60">
                <thead className={darkMode ? 'bg-slate-900/60' : 'bg-slate-50'}>
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500">Tanggal</th>
                    <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500">Deskripsi</th>
                    <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500">Kategori</th>
                    <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500">Metode</th>
                    <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-slate-500">Nominal</th>
                    <th className="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider text-slate-500">Aksi</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/40">
                  {paginatedTxs.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-6 py-10 text-center text-sm text-slate-500">
                        Tidak ada transaksi ditemukan.
                      </td>
                    </tr>
                  ) : (
                    paginatedTxs.map((t: any) => (
                      <tr key={t.id} className={darkMode ? 'hover:bg-slate-900/40' : 'hover:bg-slate-50'}>
                        <td className="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                          {new Date(t.transaction_date).toLocaleDateString('id-ID', { dateStyle: 'medium' })}
                        </td>
                        <td className="px-6 py-4 text-sm font-bold">{t.description || '-'}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">{t.category}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{t.payment_method || '-'}</td>
                        <td className={`px-6 py-4 whitespace-nowrap text-sm font-black ${t.type === 'income' ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {t.type === 'income' ? '+' : '-'} Rp {Number(t.amount).toLocaleString('id-ID')}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                          <button
                            onClick={() => removeTxMutation.mutate(t.id)}
                            className="text-slate-500 hover:text-red-400 p-1.5 transition-colors cursor-pointer"
                            title="Hapus"
                          >
                            <Trash2 className="h-4.5 w-4.5" />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>

              {/* Pagination controls */}
              <div className={`px-6 py-4 border-t ${darkMode ? 'border-slate-800/80 bg-slate-900/30' : 'border-slate-200 bg-slate-50'} flex items-center justify-between`}>
                <span className="text-xs text-slate-500">
                  Menampilkan {paginatedTxs.length} dari {filteredTxs.length} transaksi
                </span>
                <div className="flex items-center gap-2">
                  <button
                    disabled={txPage === 1}
                    onClick={() => setTxPage(txPage - 1)}
                    className="px-3 py-1.5 border border-slate-700/80 rounded-lg text-xs hover:bg-slate-800 disabled:opacity-40 disabled:hover:bg-transparent cursor-pointer"
                  >
                    Sebelumnya
                  </button>
                  <span className="text-xs font-bold px-3">
                    Halaman {txPage} dari {totalTxPages}
                  </span>
                  <button
                    disabled={txPage === totalTxPages}
                    onClick={() => setTxPage(txPage + 1)}
                    className="px-3 py-1.5 border border-slate-700/80 rounded-lg text-xs hover:bg-slate-800 disabled:opacity-40 disabled:hover:bg-transparent cursor-pointer"
                  >
                    Selanjutnya
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Notes Tab components view */}
        {activeTab === 'notes' && (
          <div className="space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-extrabold tracking-tight">Catatan Pribadi</h2>
                <p className="text-sm text-slate-500">Tulis ide, memo, dan rangkuman AI terorganisir Anda.</p>
              </div>
              <button
                onClick={() => setShowNoteModal(true)}
                className="flex items-center gap-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white text-sm font-semibold rounded-xl cursor-pointer"
              >
                <Plus className="h-4 w-4" />
                Catatan Baru
              </button>
            </div>

            {/* Search note bar */}
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="Cari judul, konten, atau tag..."
                value={noteSearch}
                onChange={(e) => setNoteSearch(e.target.value)}
                className={`w-full pl-9 pr-4 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                  darkMode ? 'bg-slate-900/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                }`}
              />
            </div>

            {/* Notes grid list */}
            {filteredNotes.length === 0 ? (
              <p className="text-sm text-slate-500 py-10 text-center">Tidak ada catatan ditemukan.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {filteredNotes.map((n: any) => (
                  <div 
                    key={n.id} 
                    className={`p-6 rounded-2xl border ${
                      darkMode ? 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-900/60' : 'bg-white border-slate-200 hover:shadow-md'
                    } flex flex-col justify-between space-y-4`}
                  >
                    <div className="space-y-3">
                      <div className="flex items-start justify-between gap-4">
                        <h3 className="font-bold text-lg text-purple-400 leading-tight">{n.title}</h3>
                        <button
                          onClick={() => removeNoteMutation.mutate(n.id)}
                          className="text-slate-500 hover:text-red-400 p-1.5 transition-colors cursor-pointer"
                          title="Hapus"
                        >
                          <Trash2 className="h-4.5 w-4.5" />
                        </button>
                      </div>
                      <p className="text-sm leading-relaxed">{n.content}</p>
                    </div>

                    <div className="space-y-2.5 pt-4 border-t border-slate-800/40">
                      <div className="flex items-center gap-1.5 text-xs text-purple-300 bg-purple-500/5 p-2 rounded-lg border border-purple-500/10">
                        <Clock className="h-3.5 w-3.5" />
                        <span><strong>Ringkasan AI:</strong> {n.summary}</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {n.tags?.map((tag: string) => (
                          <span key={tag} className="text-xs bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-md flex items-center gap-1">
                            <Tag className="h-3 w-3 text-slate-500" />
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Reports Tab components view */}
        {activeTab === 'reports' && (
          <div className="space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-extrabold tracking-tight">Analisis Keuangan</h2>
                <p className="text-sm text-slate-500">Visualisasikan dan ekspor data pembukuan Anda.</p>
              </div>
              <button
                onClick={handleExportCSV}
                className="flex items-center gap-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white text-sm font-semibold rounded-xl shadow-lg shadow-purple-500/10 cursor-pointer"
              >
                <Download className="h-4 w-4" />
                Ekspor CSV
              </button>
            </div>

            {/* Custom SVG metrics overview visualizer */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200'}`}>
                <h3 className="font-bold text-lg mb-6">Distribusi Pengeluaran Kategori</h3>
                <div className="flex flex-col items-center justify-center p-6 space-y-6">
                  {/* SVG Pie Chart simulation */}
                  <svg className="w-48 h-48 transform -rotate-90" viewBox="0 0 32 32">
                    <circle r="16" cx="16" cy="16" fill="transparent" stroke="#1f2937" strokeWidth="32" />
                    <circle r="16" cx="16" cy="16" fill="transparent" stroke="#a855f7" strokeWidth="32" strokeDasharray="60 100" />
                    <circle r="16" cx="16" cy="16" fill="transparent" stroke="#06b6d4" strokeWidth="32" strokeDasharray="30 100" strokeDashoffset="-60" />
                    <circle r="16" cx="16" cy="16" fill="transparent" stroke="#f43f5e" strokeWidth="32" strokeDasharray="10 100" strokeDashoffset="-90" />
                  </svg>
                  <div className="flex flex-wrap items-center justify-center gap-4 text-xs">
                    <div className="flex items-center gap-1.5">
                      <span className="h-3 w-3 rounded-full bg-purple-500" />
                      <span>Makanan (60%)</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="h-3 w-3 rounded-full bg-cyan-500" />
                      <span>Transportasi (30%)</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="h-3 w-3 rounded-full bg-rose-500" />
                      <span>Kopi (10%)</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommendations and AI Insights */}
              <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200'} space-y-4`}>
                <h3 className="font-bold text-lg">AI Financial Insights</h3>
                <div className="bg-purple-500/5 p-4 rounded-xl border border-purple-500/10 space-y-3">
                  <div className="flex items-center gap-1.5">
                    <CheckCircle className="h-5 w-5 text-emerald-400" />
                    <span className="font-bold text-sm text-purple-300">Rekomendasi Hemat</span>
                  </div>
                  <p className="text-sm leading-relaxed text-slate-300">
                    Pengeluaran untuk kategori <strong>Kopi</strong> dan <strong>Makanan</strong> menyumbang 70% dari anggaran bulanan Anda.
                    Cobalah kurangi intensitas memesan kopi susu di luar (hemat perkiraan Rp75.000 per minggu).
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Settings Tab components view */}
        {activeTab === 'settings' && (
          <div className="space-y-8 animate-fade-in">
            <div>
              <h2 className="text-3xl font-extrabold tracking-tight">Pengaturan</h2>
              <p className="text-sm text-slate-500">Atur profil asisten dan preferensi akun Anda.</p>
            </div>

            <div className={`p-6 rounded-2xl border ${darkMode ? 'bg-slate-900/40 border-slate-800/80' : 'bg-white border-slate-200'} max-w-xl space-y-6`}>
              <div className="space-y-4">
                <h3 className="font-bold text-lg">Konfigurasi Pengguna</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-bold uppercase text-slate-500">Nama Lengkap</label>
                    <input
                      type="text"
                      disabled
                      value={user?.full_name || ''}
                      className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none opacity-60 ${
                        darkMode ? 'bg-slate-950/40 border-slate-800 text-white' : 'bg-slate-100 border-slate-200 text-slate-900'
                      }`}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold uppercase text-slate-500">Username Telegram</label>
                    <input
                      type="text"
                      disabled
                      value={`@${user?.username || ''}`}
                      className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none opacity-60 ${
                        darkMode ? 'bg-slate-950/40 border-slate-800 text-white' : 'bg-slate-100 border-slate-200 text-slate-900'
                      }`}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold uppercase text-slate-500">Timezone</label>
                    <input
                      type="text"
                      disabled
                      value={user?.timezone || 'Asia/Jakarta'}
                      className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none opacity-60 ${
                        darkMode ? 'bg-slate-950/40 border-slate-800 text-white' : 'bg-slate-100 border-slate-200 text-slate-900'
                      }`}
                    />
                  </div>
                </div>
              </div>

              <div className="pt-6 border-t border-slate-800/60 space-y-4">
                <h3 className="font-bold text-lg">Sesi Keamanan</h3>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <p className="text-sm font-semibold">Token Web Konsol</p>
                    <p className="text-xs text-slate-500">Token JWT Anda tersimpan di cookies / memori lokal aman.</p>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 border border-red-500/30 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-semibold rounded-xl cursor-pointer"
                  >
                    Keluar Sesi
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Transaction Modal dialog */}
      {showTxModal && (
        <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className={`w-full max-w-md p-6 rounded-2xl border ${darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'} shadow-2xl space-y-6`}>
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-lg">Tambah Transaksi Baru</h3>
              <button onClick={() => setShowTxModal(false)} className="text-slate-500 hover:text-slate-300 text-sm cursor-pointer">Batal</button>
            </div>
            <form 
              onSubmit={(e) => {
                e.preventDefault();
                addTxMutation.mutate({
                  ...txForm,
                  amount: Number(txForm.amount)
                });
              }}
              className="space-y-4"
            >
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Tipe</label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setTxForm({ ...txForm, type: 'expense' })}
                    className={`py-2 text-xs font-semibold rounded-lg border ${txForm.type === 'expense' ? 'bg-rose-500/10 border-rose-500 text-rose-400' : 'border-slate-800 text-slate-400'} cursor-pointer`}
                  >
                    Pengeluaran
                  </button>
                  <button
                    type="button"
                    onClick={() => setTxForm({ ...txForm, type: 'income' })}
                    className={`py-2 text-xs font-semibold rounded-lg border ${txForm.type === 'income' ? 'bg-emerald-500/10 border-emerald-500 text-emerald-400' : 'border-slate-800 text-slate-400'} cursor-pointer`}
                  >
                    Pemasukan
                  </button>
                </div>
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Nominal (Rp)</label>
                <input
                  type="number"
                  required
                  placeholder="25000"
                  value={txForm.amount}
                  onChange={(e) => setTxForm({ ...txForm, amount: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Kategori</label>
                <input
                  type="text"
                  required
                  placeholder="Makanan / Kopi / Transportasi"
                  value={txForm.category}
                  onChange={(e) => setTxForm({ ...txForm, category: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Deskripsi</label>
                <input
                  type="text"
                  required
                  placeholder="Makan siang di warteg"
                  value={txForm.description}
                  onChange={(e) => setTxForm({ ...txForm, description: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Metode Pembayaran</label>
                <input
                  type="text"
                  required
                  placeholder="QRIS / Tunai / Debit"
                  value={txForm.payment_method}
                  onChange={(e) => setTxForm({ ...txForm, payment_method: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <button
                type="submit"
                disabled={addTxMutation.isPending}
                className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white text-sm font-semibold rounded-xl transition-all cursor-pointer"
              >
                {addTxMutation.isPending ? 'Menyimpan...' : 'Simpan Transaksi'}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Note Modal dialog */}
      {showNoteModal && (
        <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className={`w-full max-w-md p-6 rounded-2xl border ${darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'} shadow-2xl space-y-6`}>
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-lg">Catatan Baru</h3>
              <button onClick={() => setShowNoteModal(false)} className="text-slate-500 hover:text-slate-300 text-sm cursor-pointer">Batal</button>
            </div>
            <form 
              onSubmit={(e) => {
                e.preventDefault();
                const tags = noteForm.tagsString.split(',').map(t => t.trim()).filter(Boolean);
                addNoteMutation.mutate({
                  title: noteForm.title,
                  content: noteForm.content,
                  tags: tags
                });
              }}
              className="space-y-4"
            >
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Judul Catatan</label>
                <input
                  type="text"
                  required
                  placeholder="Ide Bisnis Baru"
                  value={noteForm.title}
                  onChange={(e) => setNoteForm({ ...noteForm, title: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Isi Catatan</label>
                <textarea
                  required
                  rows={4}
                  placeholder="Tulis detail ide/catatan Anda di sini..."
                  value={noteForm.content}
                  onChange={(e) => setNoteForm({ ...noteForm, content: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold uppercase text-slate-500">Tag (pisahkan dengan koma)</label>
                <input
                  type="text"
                  placeholder="bisnis, ide, finansial"
                  value={noteForm.tagsString}
                  onChange={(e) => setNoteForm({ ...noteForm, tagsString: e.target.value })}
                  className={`w-full px-3 py-2 border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-purple-500 ${
                    darkMode ? 'bg-slate-950/60 border-slate-850 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
                  }`}
                />
              </div>
              <button
                type="submit"
                disabled={addNoteMutation.isPending}
                className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white text-sm font-semibold rounded-xl transition-all cursor-pointer"
              >
                {addNoteMutation.isPending ? 'Menyimpan...' : 'Simpan Catatan'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DashboardContent />
    </QueryClientProvider>
  );
}
