# 🏦 Nsongwa Credit Union: Secure Financial Gateway v2.0
![Dashboard](dashboard.png)
**Status:** 🟢 Operational | **Security Audit:** ✅ Passed (Checkov v3.2.506)  
**Core Engine:** Dockerized Python/Flask with MoMo Integration & Automated Testing

---

## 🚀 Executive Summary
This repository contains the hardened core banking prototype for **Nsongwa Credit Union**. It transitions traditional manual ledgering into a secure, digital-first environment capable of handling real-time member transactions, mobile money (MoMo) simulation, and automated test coverage.

## 🔐 Advanced Security Features
* **Cryptographic Identity**: Member PINs are never stored in plain text; we use **SHA-256 Hashing** to ensure data privacy.
* **Non-Root Execution**: The application runs under a restricted security profile within Docker to prevent system-level breaches.
* **Infrastructure-as-Code Auditing**: Scanned by **Checkov** to meet international financial security standards.
* **Session Management**: Secure server-side sessions protect members from unauthorized account access during active use.

## 📱 Integrated Services & Features
* **Member Portal**: Secure member registration, login, and real-time balance inquiry.
* **Mobile Money (MoMo) & Withdrawal Gateways**: Instant deposit and withdrawal functionality from digital wallets.
* **Automated Testing Suite**: Full `pytest` integration validating routing, registration, and authentication workflows.
* **Statement Download**: Exportable text-based transaction ledger for individual members.
* **Live Audit Ledger**: Real-time transaction history tracking for financial transparency.

## 🛠️ Technical Stack
* **Language**: Python 3.9+ / Python 3.14 compatible framework.
* **Framework**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended.
* **Testing**: Pytest for unit and integration checks.
* **Server**: Gunicorn production-grade WSGI application server.
* **Orchestration**: Docker & Docker Compose for service availability.
* **Database**: SQLite (Development) / PostgreSQL-ready architecture.

---

## 🚀 How to Run the Demo

1. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate
Run the Test Suite (Pytest):

Bash
pytest -v
Start the Production Server (Gunicorn):

Bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
Access the Portal:

Open your browser and navigate to http://127.0.0.1:5000.

🚀 Future Roadmap (v3.0 & Beyond)
🗄️ Database Migration: Transitioning the persistence layer to a fully-managed PostgreSQL database.

🔐 Multi-Factor Authentication (MFA): Adding SMS/Email OTP verification for high-value transactions.

📊 Financial Analytics Dashboard: Implementing Chart.js to provide visual savings trends.

☁️ Cloud CI/CD Pipelines: Automated deployments via GitHub Actions into hardened containers.

👤 Author & Developer
Name: Frank Fru

Email: chifru19@googlemail.com

Website: frankfru.com

GitHub: chifru19

LinkedIn: Frank Fru LinkedIn Profile

© 2026 Nsongwa Credit Union Digital Transformation Project