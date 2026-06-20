# Testing
Testing Strategy

Gunakan pendekatan berikut:

Unit Test
Integration Test
End-to-End Test

Target code coverage minimum:

80%
Backend Testing

Framework:

pytest
pytest-asyncio
httpx

Jalankan:

pytest

Coverage:

pytest --cov=app
Frontend Testing

Framework:

Vitest
React Testing Library

Jalankan:

npm run test
End-to-End Testing

Framework:

Playwright

Jalankan:

npm run test:e2e
Test Structure
tests/
├── unit/
├── integration/
├── e2e/
└── fixtures/
CI Requirements

Pull Request tidak dapat digabungkan jika:

Test gagal
Coverage di bawah 80%
Linter gagal