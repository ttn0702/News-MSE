# Sử dụng image Nginx chính thức
FROM nginx:latest

# Xóa file default.conf mặc định của Nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# Sao chép các file HTML, CSS và JS vào thư mục mặc định của Nginx
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY scripts.js /usr/share/nginx/html/

# Sao chép file cấu hình Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Expose port 80 để truy cập từ bên ngoài
EXPOSE 80
