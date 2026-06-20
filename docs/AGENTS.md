# AI Agents

## Overview

Sistem menggunakan pendekatan multi-agent.

Setiap agent memiliki tanggung jawab spesifik.

---

## 1. Router Agent

Responsibilities:

* Mendeteksi intent
* Meneruskan request

Supported intents:

* expense
* income
* note
* report
* reminder
* unknown

---

## 2. Expense Agent

Input:

"Beli kopi 20 ribu"

Output:

```json
{
  "intent": "expense",
  "amount": 20000,
  "category": "Makanan",
  "description": "Kopi"
}
```

Responsibilities:

* Klasifikasi kategori
* Ekstraksi nominal
* Validasi transaksi

---

## 3. Note Agent

Responsibilities:

* Menyimpan catatan
* Membuat tag
* Membuat ringkasan

---

## 4. Report Agent

Responsibilities:

* Analisis data
* Ringkasan bulanan
* Insight pengeluaran

---

## 5. Reminder Agent

Responsibilities:

* Pengingat tagihan
* Pengingat tugas

---

## 6. Fallback Agent

Responsibilities:

* Menangani input ambigu
* Meminta klarifikasi

Contoh:

"Makan 20"

Respons:

"Apakah Rp20.000 atau Rp20?"
