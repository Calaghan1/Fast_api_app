FROM python:3.10-slim
RUN mkdir -p /app
WORKDIR /Fast_api_app

COPY requirements.txt /
RUN pip install --requirement /requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
