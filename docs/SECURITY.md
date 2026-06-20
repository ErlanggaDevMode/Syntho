# Security Guidelines

## Authentication

* JWT Access Token
* Refresh Token

## Authorization

* Role Based Access Control

Roles:

* admin
* user

## Data Protection

* HTTPS only
* Password hashing dengan Argon2
* Enkripsi backup database
* Environment variables untuk secrets

## AI Security

* Validasi output AI
* Jangan izinkan AI mengakses database secara langsung
* Gunakan JSON schema validation

## Telegram Security

* Verifikasi webhook signature
* Rate limiting
* Anti-spam
