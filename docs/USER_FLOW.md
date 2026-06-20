## User Flow: Expense Tracking

1. **User sends message**
   `Makan siang di warteg 25 ribu`

2. **Telegram Bot receives**
   Validasi webhook signature

3. **Router Agent**
   Dideteksi: `expense`
   Meneruskan ke Expense Agent

4. **Expense Agent**
   Ekstraksi entitas:
   - amount: 25000
   - category: Makanan
   - description: Makan siang di warteg
   - payment_method: Tunai
   - transaction_date: [timestamp]

5. **Backend API**
   Validasi data
   Simpan ke PostgreSQL

6. **Response**
   ✅ Transaksi dicatat:
   🍽️ Makan siang di warteg: Rp25.000

## User Flow: Note

1. **User sends note**
   `Ide: buat aplikasi chatbot AI untuk keuangan`

2. **Telegram Bot receives**
   Meneruskan ke Note Agent

3. **Note Agent**
   Ekstraksi entitas:
   - title: Ide Chatbot Keuangan
   - summary: Ide untuk membuat aplikasi chatbot AI finansial
   - tags: [idea, chatbot, finance]

4. **Backend API**
   Simpan ke PostgreSQL

5. **Response**
   📝 Catatan tersimpan: Ide Chatbot Keuangan

## User Flow: Report Generation

1. **User requests report**
   `Laporan minggu ini`

2. **Router Agent**
   Dideteksi: `report`

3. **Report Agent**
   Analisis data minggu ini
   - Total pengeluaran
   - Kategori teratas
   - Tren mingguan

4. **Response**
   📊 Laporan Minggu Ini:
   Total: Rp1.250.000
   Makanan: Rp450.000
   Transportasi: Rp300.000
   Kopi: Rp150.000
