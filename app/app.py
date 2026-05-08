from flask import Flask, request, redirect, render_template
import redis
import random
import string
import json
from datetime import datetime

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, db=0)


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>

    <head>

        <title>DevOps URL Shortener</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #4facfe, #00f2fe);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0px 5px 20px rgba(0,0,0,0.2);
                width: 500px;
                text-align: center;
            }

            h1 {
                color: #2c3e50;
                margin-bottom: 25px;
            }

            input {
                width: 70%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
            }

            button {
                padding: 12px 18px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                margin-left: 10px;
            }

            button:hover {
                background: #0056b3;
            }

            .footer {
                margin-top: 20px;
                color: gray;
                font-size: 14px;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>DevOps URL Shortener</h1>

            <form action="/shorten" method="post">

                <input
                    type="text"
                    name="url"
                    placeholder="Enter your long URL"
                    required
                >

                <button type="submit">
                    Shorten
                </button>

            </form>

            <div class="footer">
                Flask • Redis • Docker • Jenkins
            </div>

        </div>

    </body>

    </html>
    '''


@app.route('/shorten', methods=['POST'])
def shorten_url():

    url = request.form.get('url')

    short_code = generate_short_code()

    r.set(short_code, url)

    short_url = request.host_url + short_code

    return f'''
    <!DOCTYPE html>
    <html>

    <head>

        <title>Short URL Created</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}

            .container {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0px 5px 20px rgba(0,0,0,0.1);
                width: 500px;
                text-align: center;
            }}

            h2 {{
                color: #2c3e50;
            }}

            a {{
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }}

            .dashboard {{
                margin-top: 20px;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h2>Short URL Created Successfully</h2>

            <p>
                <a href="{short_url}">
                    {short_url}
                </a>
            </p>

            <div class="dashboard">

                <a href="/dashboard/{short_code}">
                    View Analytics Dashboard
                </a>

            </div>

        </div>

    </body>

    </html>
    '''


@app.route('/<short_code>')
def redirect_url(short_code):

    original_url = r.get(short_code)

    if original_url:

        r.incr(f"clicks:{short_code}")

        analytics_data = {
            "browser": str(request.user_agent),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        r.rpush(
            f"analytics:{short_code}",
            json.dumps(analytics_data)
        )

        return redirect(original_url.decode("utf-8"))

    return "URL not found"


@app.route('/dashboard/<short_code>')
def dashboard(short_code):

    clicks = r.get(f"clicks:{short_code}")

    if clicks is None:
        clicks = 0
    else:
        clicks = int(clicks)

    analytics = r.lrange(f"analytics:{short_code}", 0, -1)

    analytics = [json.loads(item) for item in analytics]

    return render_template(
        'dashboard.html',
        short_code=short_code,
        clicks=clicks,
        analytics=analytics
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)