# Sử dụng image Python chính thức
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file Python vào thư mục làm việc
COPY . /app

# Cài đặt các phụ thuộc (nếu có)
# Giả sử bạn có một requirements.txt cho các thư viện cần thiết
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Chạy ứng dụng
CMD ["python", "main.py"]