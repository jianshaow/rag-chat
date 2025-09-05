import os

backend_base_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

files_url_prefix = "/api/files"
files_base_url = f"{backend_base_url}{files_url_prefix}"
