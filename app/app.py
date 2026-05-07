from flask import Flask, request, redirect, render_template
import redis
import random
import string

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def home():

    short_url = None

    if request.method == 'POST':

        long_url = request.form['url']

        short_code = generate_code()

        r.set(short_code, long_url)

        short_url = f"http://localhost:5000/{short_code}"

    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_url(short_code):

    long_url = r.get(short_code)

    if long_url:
        return redirect(long_url)

    return "URL not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)