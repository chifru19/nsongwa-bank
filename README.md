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
Nsongwa Credit Union - Secure Banking Portal
A professional-grade Flask banking application focused on security and real-time transaction processing.

🛡️ Security Implementation
This project uses industry-standard security patterns to protect customer data:

Environment Secret Management: We use os.getenv for the app.secret_key to keep sensitive encryption keys out of the source code.

Fail-Safe Configuration: Line 6 includes a fallback string to prevent "Internal Server Errors" if the environment file is missing.

Cryptographic PIN Hashing: User PINs are stored as SHA-256 hashes. Even if the database is accessed, the actual PINs remain unreadable.

Session Isolation: Each login creates a unique, encrypted session that must be active to view the dashboard.

💻 Tech Stack
Backend: Python 3 with Flask.

Environment: Isolated venv (Virtual Environment) for secure dependency management.

Frontend: HTML/CSS with dynamic Jinja2 templating.

🚀 How to Run the Demo
Activate the Environment: source venv/bin/activate.

Start the Server: python3 app.py.

Access the Portal: Open http://127.0.0.1:5000.
![Nsongwa Bank Dashboard](assets/dashboard.png)
