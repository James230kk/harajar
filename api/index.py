from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Haraj API running on Vercel!"}

# Vercel handler
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)