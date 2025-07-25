---

# 🎬 API Backend Website Xem Phim (Django + PostgreSQL)

Đây là hệ thống backend đơn giản phục vụ cho một website xem phim. Dự án này cung cấp các API REST để:

- Xem danh sách phim
- Xem chi tiết từng phim
- Xem video của phim
- Thêm / sửa / xóa phim thông qua API

---

## 🚀 Công nghệ sử dụng

- Python 3
- Django & Django REST Framework
- PostgreSQL (Render cung cấp miễn phí)
- Gunicorn (chạy production)
- Render.com (triển khai hosting)

---

## 🔧 Hướng dẫn chạy dự án trên máy cá nhân (Windows / macOS / Linux)

### 1. Clone dự án

```bash
git clone https://github.com/dangscotlptit/BE.git
cd BE
````

### 2. Tạo môi trường ảo và kích hoạt

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Tạo file `.env`

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/movie_db
```

> Nếu dùng MySQL: đổi `DATABASE_URL` cho phù hợp.

---

### 5. Chạy migrate và khởi động server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🌐 Danh sách API

| Method | Endpoint                  | Chức năng          |
| ------ | ------------------------- | ------------------ |
| GET    | `/api/movies/`            | Lấy danh sách phim |
| POST   | `/api/movies/`            | Thêm phim mới      |
| GET    | `/api/movies/<id>/`       | Chi tiết phim      |
| PUT    | `/api/movies/<id>/`       | Cập nhật phim      |
| DELETE | `/api/movies/<id>/`       | Xoá phim           |
| GET    | `/api/movies/<id>/watch/` | Lấy link xem phim  |

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
├── .env (không push lên GitHub)
```

---

