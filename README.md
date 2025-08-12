# BloodHub

A full-stack web application that connects blood donors and receivers with the nearest donation centres.  
Users can register as a **Donor** or **Receiver**, fill in basic details, and instantly see the closest blood donation facility.

---

## Features

- **Role-based signup** — Choose to sign up as a Donor or Receiver.
- **Data capture** — Collects basic details like name, blood group, location, and contact info.
- **Location-based suggestions** — After submitting, shows the nearest blood donation centre.
- **Full-stack architecture** — Flask backend with database storage and responsive frontend.
- **Search optimisation** — Matches donors and receivers in the same area.

---

## Tech Stack

**Frontend:** HTML, CSS (Tailwind), JavaScript  
**Backend:** Python (Flask)  
**Database:** SQLite (or replace with MySQL/PostgreSQL)  

---

## How It Works

1. **User Registration**
   - Choose role: Donor or Receiver
   - Fill personal details and location

2. **Data Storage**
   - Information saved in database

3. **Centre Locator**
   - Uses GoMaps API to find nearest blood donation centre
   - Displays name, address, and distance

4. **Results**
   - Donor list accessible to receivers
   - Receiver requests visible to donors

---

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Steps
```bash
# Clone the repository
git clone https://github.com/<your-username>/BloodHub.git
cd BloodHub

# Install dependencies
pip install -r requirements.txt

# Set environment variables (Linux/Mac example)
export FLASK_APP=app.py
export FLASK_ENV=development

# For Windows PowerShell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

# Run the server
flask run
