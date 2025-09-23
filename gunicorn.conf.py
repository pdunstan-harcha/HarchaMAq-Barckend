# Gunicorn configuration file for Railway deployment
import multiprocessing
import os

# Railway uses the PORT environment variable
port = os.getenv("PORT", "5000")
bind = f"0.0.0.0:{port}"

# Optimize for Railway's container resources
workers = int(os.getenv("GUNICORN_WORKERS", min(multiprocessing.cpu_count() * 2, 4)))
threads = int(os.getenv("GUNICORN_THREADS", 4))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")

# Logging
accesslog = os.getenv("GUNICORN_ACCESSLOG", "-")  # stdout
errorlog = os.getenv("GUNICORN_ERRORLOG", "-")   # stderr
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")

# Timeouts optimized for Railway
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 10))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", 30))

# Memory management
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 100))

# Enable preload for better performance
preload_app = True

print(f"Gunicorn configurado para Railway - Bind: {bind}, Workers: {workers}, Threads: {threads}")
