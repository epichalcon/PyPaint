# PyPaint

This is an implementation of the famous Paint By Numbers idea in python. It has been developed as a proyect for the AI Lab subject in La Sapienza university of Rome.

## Setup

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/epichalcon/PyPaint.git
cd PyPaint

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

export FLASK_APP=backend  # On Windows, use `set FLASK_APP=app.py`
export FLASK_ENV=development  # On Windows, use `set FLASK_ENV=development`
flask run
```

After executing these steps, access the program on localhost:5000 (preferably with chrome)
