# AI Notes & Expense Tracker

## 1. Overview

AI Notes & Expense Tracker adalah aplikasi pencatatan pengeluaran dan catatan pribadi berbasis AI yang terintegrasi dengan Telegram.

Pengguna dapat mencatat transaksi dan catatan menggunakan bahasa alami melalui Telegram, kemudian sistem akan mengklasifikasikan, menyimpan, menganalisis, dan menghasilkan laporan otomatis.

Tujuan utama produk adalah menghilangkan kebutuhan input manual yang rumit.

Contoh:

* "Beli kopi 20 ribu"
* "Isi bensin 50 ribu pakai QRIS"
* "Catatan: ide konten Instagram minggu depan"
* "Gaji masuk 3 juta"

AI akan memahami konteks dan menyimpan data secara otomatis.

---

## 2. Problem Statement

Permasalahan yang ingin diselesaikan:

* Pengguna malas membuka aplikasi keuangan.
* Pencatatan pengeluaran sering terlupakan.
* Catatan pribadi tersebar di banyak platform.
* Pembuatan laporan membutuhkan waktu.
* Pengguna kesulitan menganalisis pola keuangan.

---

## 3. Goals

### Business Goals

* Membangun asisten pencatat pribadi berbasis AI.
* Menyediakan laporan otomatis.
* Menjadi platform yang dapat dikembangkan menjadi personal assistant.

### User Goals

* Mencatat pengeluaran dalam kurang dari 10 detik.
* Mengakses laporan kapan saja.
* Menyimpan catatan dan transaksi di satu tempat.
* Mendapatkan insight otomatis.

---

## 4. Success Metrics

* Akurasi klasifikasi transaksi ≥ 90%
* Waktu respons bot ≤ 5 detik
* Tingkat keberhasilan parsing ≥ 95%
* Tingkat kegagalan penyimpanan < 1%
* Pengguna aktif mingguan > 70%

---

## 5. User Personas

### Mahasiswa

* Mengelola uang saku
* Mencatat tugas dan ide

### Pekerja

* Mencatat pengeluaran harian
* Memantau anggaran bulanan

### Organisasi

* Mencatat kas dan kegiatan

---

## 6. Core Features

### Expense Tracking

* Catat pemasukan
* Catat pengeluaran
* Kategori otomatis
* Edit transaksi
* Hapus transaksi
* Filter transaksi

### Note Taking

* Catatan teks bebas
* Tag otomatis
* Pencarian catatan
* Ringkasan AI

### AI Reporting

* Laporan harian
* Laporan mingguan
* Laporan bulanan
* Analisis tren

### Telegram Integration

* Input bahasa alami
* Notifikasi
* Pengingat

### Dashboard

* Grafik pengeluaran
* Kalender transaksi
* Export Excel
* Export PDF

---

## 7. Non-Functional Requirements

* Mobile friendly
* Multi-user
* Data terenkripsi
* Mendukung bahasa Indonesia
* Arsitektur modular
* Self-hosted

---

## 8. Constraints

* Mengutamakan solusi gratis.
* Dapat berjalan pada PC spesifikasi rendah.
* Tidak bergantung pada layanan berbayar.
* Mendukung deployment lokal.

---

## 9. MVP Scope

### Included

* Telegram Bot
* Input transaksi
* Input catatan
* Klasifikasi AI
* Dashboard sederhana
* Laporan bulanan

### Excluded

* OCR struk
* Voice input
* Integrasi bank
* Multi-currency
* Aplikasi mobile native
