# Database Schema

## users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    full_name VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'Asia/Jakarta',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## transactions

```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),

    type VARCHAR(20) NOT NULL,
    amount NUMERIC(15,2) NOT NULL,

    category VARCHAR(100),

    description TEXT,

    payment_method VARCHAR(50),

    transaction_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW()
);
```

## notes

```sql
CREATE TABLE notes (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),

    title VARCHAR(255),

    content TEXT,

    tags JSONB,

    summary TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);
```

## reminders

```sql
CREATE TABLE reminders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),

    title VARCHAR(255),

    due_date TIMESTAMP,

    status VARCHAR(20),

    created_at TIMESTAMP DEFAULT NOW()
);
```
