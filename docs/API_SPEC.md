# API Specification

## Base URL

```text
/api/v1
```

## Authentication

* Telegram Login Widget
* JWT Access Token

---

## Transactions

### Create Transaction

```http
POST /transactions
```

### Get Transactions

```http
GET /transactions
```

### Update Transaction

```http
PUT /transactions/{id}
```

### Delete Transaction

```http
DELETE /transactions/{id}
```

---

## Notes

```http
POST /notes
GET /notes
PUT /notes/{id}
DELETE /notes/{id}
```

---

## Reports

```http
GET /reports/monthly
GET /reports/weekly
GET /reports/daily
```

---

## AI

```http
POST /ai/parse
POST /ai/summarize
```
