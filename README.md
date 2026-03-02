# 🏦 Nsongwa Credit Union: Secure Financial Gateway v2.0

**Status:** 🟢 Operational | **Security Audit:** ✅ Passed (Checkov v3.2.506)
**Core Engine:** Dockerized Python/Flask with MoMo Integration

---

## 🚀 Executive Summary
This repository contains the hardened core banking prototype for **Nsongwa Credit Union**. It transitions traditional manual ledgering into a secure, digital-first environment capable of handling real-time member transactions.

## 🔐 Advanced Security Features
* **Cryptographic Identity**: Member PINs are never stored in plain text; we use **SHA-256 Hashing** to ensure data privacy.
* **Non-Root Execution**: The application runs under a restricted `bankuser` profile within Docker to prevent system-level breaches.
* **Infrastructure-as-Code Auditing**: Scanned by **Checkov** to meet international financial security standards.
* **Session Management**: Secure server-side sessions protect members from unauthorized account access during active use.

## 📱 Integrated Services (Phase 1)
* **Member Portal**: Secure login and real-time balance inquiry.
* **Mobile Money (MoMo) Gateway**: Instant deposit functionality from mobile wallets (MTN/Orange simulation).
* **Live Audit Ledger**: Real-time transaction history tracking for financial transparency.

## 🛠️ Technical Stack
* **Language**: Python 3.9-slim (Hardened Base Image).
* **Orchestration**: Docker Compose for "Self-Healing" service availability.
* **Security Scanner**: Bridgecrew Checkov.
* **Database**: PostgreSQL (Production Ready).

---
*© 2026 Nsongwa Credit Union Digital Transformation Project*