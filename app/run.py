# backend/run.py
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")
    app.run(host='0.0.0.0', port=5000, debug=debug)