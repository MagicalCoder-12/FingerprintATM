# Fingerprint Based ATM System

A Flask web application that simulates ATM operations with **fingerprint biometric authentication**. Users register with a fingerprint image, and subsequent logins require matching the uploaded fingerprint against the stored image along with username/password credentials.

## Features

- **User Registration** — Collects username, password, contact, email, address, gender, and a fingerprint image (stored as `static/users/<username>.png`)
- **Fingerprint Authentication** — Login verifies credentials via byte-level comparison of the uploaded fingerprint against the stored image
- **ATM Operations**
  - Deposit funds
  - Withdraw funds (with insufficient-funds check)
  - View transaction history and current balance
- **Persistence** — MongoDB backend with `users` and `transactions` collections

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Flask |
| Database | MongoDB (via `pymongo`) |
| Frontend | HTML templates + CSS (`templates/`, `static/`) |
| Biometric Storage | File-system PNG images (`static/users/`, `BiometricImages/`) |

## Project Structure

```
FingerprintATM/
├── Main.py              # Flask app — all routes and DB logic
├── run.bat              # Windows helper to activate conda and run Main.py
├── templates/           # Jinja2 HTML templates
│   ├── index.html       # Landing page
│   ├── Login.html       # Login form (username, password, fingerprint upload)
│   ├── Signup.html      # Registration form
│   ├── UserScreen.html  # Post-login dashboard
│   ├── Deposit.html     # Deposit form
│   ├── Withdraw.html    # Withdraw form
│   └── ViewBalance.html # Transaction history table
├── static/
│   ├── default.css / style.css
│   ├── tra.jpg, img*.jpg
│   └── users/           # Stored fingerprint images per user (e.g., Ajith.png)
├── BiometricImages/     # Sample fingerprint images (1.png, 2.png, 3.png, 4.png)
└── 36.Fingerprint based on ATM System.docx  # Project documentation
```

## Prerequisites

- Python 3.8+
- MongoDB running locally on `mongodb://localhost:27017/`
- `pip` packages: `flask`, `pymongo`

## Installation

```bash
git clone <repo-url>
cd FingerprintATM

# (optional) create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install flask pymongo

# ensure MongoDB is running
# e.g., mongod --dbpath /data/db

# create the fingerprint storage directory if missing
mkdir -p static/users
```

Ensure a MongoDB database named `atm` is accessible. Collections `users` and `transactions` are created automatically on first write.

## Usage

### Run the app

```bash
python Main.py
# or on Windows
run.bat
```

The app starts at `http://127.0.0.1:5000/` (Flask debug mode, auto-redirects `/` → `/index`).

### Workflow

1. **Signup** — Navigate to `Signup Here`, fill in details, and upload a fingerprint image.
2. **Login** — Navigate to `Login Here`, enter username/password and upload the same fingerprint image. Authentication is a direct byte comparison (`Main.py:88`).
3. **ATM Operations** — After login:
   - **Deposit** — Enter amount to credit (`/Deposit` → `/DepositAction`).
   - **Withdraw** — Enter amount to debit; rejected if balance is insufficient (`/Withdraw` → `/WithdrawAction`).
   - **View Balance** — Lists all transactions with running `total_balance` (`/ViewBalance`).
   - **Logout** — Returns to the home page.

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirects to `/index` |
| `/index` | GET | Home page |
| `/Login` | GET | Login form |
| `/Signup` | GET | Signup form |
| `/SignupAction` | POST | Creates user document + saves fingerprint PNG |
| `/LoginAction` | POST | Validates username/password + fingerprint bytes |
| `/Deposit` | GET | Deposit form (pre-fills logged-in user) |
| `/DepositAction` | POST | Inserts deposit transaction, updates balance |
| `/Withdraw` | GET | Withdraw form |
| `/WithdrawAction` | POST | Inserts withdrawal transaction if funds suffice |
| `/ViewBalance` | GET | Renders transaction history for current user |
| `/Logout` | GET | Redirects to `/index` |

## Database Schema

**`atm.users`**
```json
{
  "username": "string",
  "password": "string",
  "contact_no": "string",
  "emailid": "string",
  "address": "string",
  "gender": "string"
}
```

**`atm.transactions`**
```json
{
  "username": "string",
  "transaction_amount": "number",
  "transaction_type": "Deposit | Withdrawal",
  "transaction_date": "YYYY-MM-DD HH:MM:SS",
  "total_balance": "number"
}
```

Fingerprint images are stored outside the DB at `static/users/<username>.png`.

## Configuration

- MongoDB URI: `mongodb://localhost:27017/` (`Main.py:11`)
- Database name: `atm` (`Main.py:12`)
- Flask secret key: `welcome` (`Main.py:7`) — change before deploying
- Server: `app.run(debug=True)` — disable debug in production

## Limitations & Future Work

- Fingerprint matching is exact byte equality, not biometric feature extraction — any image re-encoding will cause a mismatch.
- No password hashing; credentials are stored in plaintext.
- Global `uname` variable is not thread-safe for concurrent users — use Flask `session` instead.
- No CSRF protection or input sanitization.
- Potential improvements: image hashing / minutiae matching (e.g., OpenCV), bcrypt, Flask-Login, and proper session management.

## License

This project is open source. No license file has been added yet — if you plan to publish it, consider adding one (e.g., MIT, Apache-2.0, GPL) as a `LICENSE` file in the repository root.
