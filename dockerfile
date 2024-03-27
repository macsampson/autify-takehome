FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./fetch.py"]
CMD []

# To run the container, use the following command:
# docker run -v /path/to/output:/app <image_id>