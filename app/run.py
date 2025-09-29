# backend/run.py
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)