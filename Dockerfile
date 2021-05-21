FROM python:3

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD gunicorn -b 0.0.0.0:5000 'app:create_app()'