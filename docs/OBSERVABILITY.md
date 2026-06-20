# Observability

Monitoring Stack

Gunakan:

Prometheus
Grafana
Loki
OpenTelemetry
Metrics
API
Request count
Error rate
Response time
Active users
AI
Model latency
Parsing accuracy
Token usage
Failed requests
Database
Query duration
Connection count
Storage usage
Logging

Gunakan structured logging JSON.

Contoh:

{
  "timestamp": "2026-06-20T10:00:00Z",
  "service": "backend",
  "level": "INFO",
  "user_id": "uuid",
  "message": "Transaction created"
}

Jangan pernah mencatat:

Password
JWT token
Telegram token
Data sensitif pengguna
Tracing

Gunakan OpenTelemetry untuk:

Telegram Bot
Backend API
AI Service
Database query
Alerting

Buat alert jika:

Error rate > 5%
API latency > 3 detik
Disk usage > 85%
AI service offline