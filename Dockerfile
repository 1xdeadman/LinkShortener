FROM python:3

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY src src


ENV WEB_HOST='0.0.0.0'
ENV WEB_PORT='5000'

CMD gunicorn -b ${WEB_HOST}:${WEB_PORT} 'src.app:create_app()'