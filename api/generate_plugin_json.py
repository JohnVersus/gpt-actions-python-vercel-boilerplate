import json
import os
from dotenv import load_dotenv

load_dotenv()


def generate_plugin_info_file() -> json:
    token = os.getenv("GPT_API_KEY")
    if not token:
        print("Verification token not found in environment variable.")
        return
    plugin_info = {
        "schema_version": "v1",
        "name_for_human": "Book Collection",
        "name_for_model": "bookStore",
        "description_for_human": "A simple plugin to add books to an open collection of books.",
        "description_for_model": "A simple plugin to add books to an open collection of books. You can add new books, view existing books, view books by Id's or delete books by id.",
        "auth": {
            "type": "service_http",
            "authorization_type": "bearer",
            "verification_tokens": {"openai": token},
        },
        "api": {
            "type": "openapi",
            "url": "https://chatgpt-plugin-python-vercel-boilerplate.vercel.app/openapi.json",
        },
        "logo_url": "https://chatgpt-plugin-python-vercel-boilerplate.vercel.app/static/logo.png",
        "contact_email": "admin@johnversus.dev",
        "legal_info_url": "https://chatgpt-plugin-python-vercel-boilerplate.vercel.app/static/legal",
    }

    return plugin_info
