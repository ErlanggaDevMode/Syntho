# Code Style

Backend
Python 3.12+
Gunakan type hints
Ikuti PEP 8
Maksimal 100 karakter per baris
Gunakan docstring Google Style

Formatter:

Black
Ruff
isort

Format kode:

black .
ruff check .
isort .
Frontend
TypeScript wajib
Functional component
React Hooks
Hindari class component

Formatter:

ESLint
Prettier

Format kode:

npm run lint
npm run format
API Design

Gunakan pola REST.

Contoh:

GET    /api/v1/transactions
POST   /api/v1/transactions
PUT    /api/v1/transactions/{id}
DELETE /api/v1/transactions/{id}

Gunakan snake_case untuk database dan camelCase untuk frontend.

Naming Convention
Python
class ExpenseService:
    pass

def create_transaction():
    pass
React
export function TransactionCard() {}