# Deployment Guide

## Stack

* Docker
* Docker Compose

## Services

* frontend
* backend
* postgres
* redis
* ollama
* telegram-bot

## Requirements

Minimum:

* CPU: 4 core
* RAM: 8 GB
* Storage: SSD 256 GB

Recommended:

* CPU: 6 core
* RAM: 16 GB
* Storage: SSD 512 GB

## Access From Anywhere

Options:

* Cloudflare Tunnel
* Tailscale

Recommended:

* Tailscale untuk akses pribadi
* Cloudflare Tunnel untuk dashboard publik

## Backup Strategy

* Daily PostgreSQL dump
* Weekly full backup
* Backup retention 30 hari
