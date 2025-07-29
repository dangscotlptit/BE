---
Test api: https://be-k3g5.onrender.com/api/
---

# API Backend Website Xem Phim (Django + PostgreSQL)

Đây là hệ thống backend đơn giản phục vụ cho một website xem phim. Dự án cung cấp các API REST để:

- Xem danh sách phim
- Xem chi tiết từng phim
- Tìm kiếm phim theo tiêu đề
- Xem video của phim
- Thêm / sửa / xoá phim (chỉ dành cho tài khoản admin)

---

## Công nghệ sử dụng

- Python 3
- Django & Django REST Framework
- PostgreSQL (Render cung cấp miễn phí)
- JWT (xác thực bằng token)
- Gunicorn (production server)
- Render.com (triển khai hosting miễn phí)

---

## Hướng dẫn chạy trên máy cá nhân (Windows/macOS/Linux)

### 1. Clone dự án

```bash
git clone https://github.com/dangscotlptit/BE.git
cd BE
````

### 2. Tạo môi trường ảo & kích hoạt

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Cài thư viện

```bash
pip install -r requirements.txt
```

### 4. Tạo file `.env`

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/movie_db
```

---

### 5. Chạy migrate & server

```bash
python manage.py migrate
python manage.py runserver
```

---

## Danh sách API

| Method | Endpoint                  | Chức năng                           | Quyền truy cập |
| ------ | ------------------------- | ----------------------------------- | -------------- |
| GET    | `/api/movies/`            | Lấy danh sách phim, hỗ trợ `search` | Mọi người      |
| POST   | `/api/movies/`            | Thêm phim mới                       | Chỉ admin      |
| GET    | `/api/movies/<id>/`       | Chi tiết phim                       | Mọi người      |
| PUT    | `/api/movies/<id>/`       | Cập nhật phim                       | Chỉ admin      |
| DELETE | `/api/movies/<id>/`       | Xoá phim                            | Chỉ admin      |
| GET    | `/api/movies/<id>/watch/` | Lấy link xem phim                   | Mọi người      |
| POST   | `/api/token/`             | Đăng nhập, nhận JWT token           | Chỉ admin      |
| POST   | `/api/token/refresh/`     | Làm mới access token                | Chỉ admin      |

---

## Xác thực người dùng (JWT)

* Tạo tài khoản admin:

  ```bash
  python manage.py createsuperuser
  ```

* Đăng nhập bằng API:

  ```http
  POST /api/token/
  Content-Type: application/json
  {
    "username": "admin",
    "password": "yourpassword"
  }
  ```

* Gửi các request có yêu cầu quyền bằng:

  ```http
  Authorization: Bearer <access_token>
  ```

---

## Tìm kiếm phim theo tiêu đề

```http
GET /api/movies/?search=batman
```

Trả về danh sách phim có từ khoá "batman" trong tiêu đề.

---

## Ví dụ dữ liệu phim (JSON)

```json
{
  "title": "Inception",
  "description": "Phim khoa học viễn tưởng",
  "video_url": "https://example.com/inception.mp4",
  "poster_url": "https://example.com/inception.jpg",
  "release_year": 2010
}
```

---

## Cấu trúc dự án

```
movie_site/
├── movies/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── movie_site/
│   ├── settings.py
│   ├── urls.py
├── manage.py
├── requirements.txt
├── Procfile
├── .env (không commit)
```

---

