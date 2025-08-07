Dưới đây là bản **cập nhật đầy đủ `README.md`** với nội dung:

* ✅ Tách riêng API cho **bình luận** và **đánh giá** phim
* ✅ Giải thích rõ chức năng và cách sử dụng từng API
* ✅ Cập nhật bảng API mới
* ✅ Ví dụ `POST` dữ liệu đánh giá / bình luận

---

### ✅ `README.md` (đã cập nhật)

````markdown
---
Test api: https://be-k3g5.onrender.com/
---

# API Backend Website Xem Phim (Django + PostgreSQL)

Dự án backend đơn giản cho một website xem phim, cung cấp các API REST để:

- Xem danh sách phim
- Xem chi tiết từng phim
- Tìm kiếm phim theo tiêu đề
- Xem video của phim
- Bình luận và đánh giá phim (tách riêng)
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

## Hướng dẫn chạy trên máy cá nhân

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

| Method | Endpoint                     | Chức năng                       | Quyền truy cập |
| ------ | ---------------------------- | ------------------------------- | -------------- |
| GET    | `/api/movies/`               | Lấy danh sách phim (`search`)   | Mọi người      |
| POST   | `/api/movies/`               | Thêm phim mới                   | Chỉ admin      |
| GET    | `/api/movies/<id>/`          | Chi tiết phim + điểm trung bình | Mọi người      |
| PUT    | `/api/movies/<id>/`          | Cập nhật phim                   | Chỉ admin      |
| DELETE | `/api/movies/<id>/`          | Xoá phim                        | Chỉ admin      |
| GET    | `/api/movies/<id>/watch/`    | Lấy link xem phim               | Mọi người      |
| GET    | `/api/movies/<id>/comments/` | Xem bình luận                   | Mọi người      |
| POST   | `/api/movies/<id>/comments/` | Gửi bình luận                   | Mọi người      |
| GET    | `/api/movies/<id>/ratings/`  | Xem danh sách đánh giá          | Mọi người      |
| POST   | `/api/movies/<id>/ratings/`  | Gửi đánh giá (1–5 sao)          | Mọi người      |
| POST   | `/api/token/`                | Đăng nhập, nhận JWT token       | Chỉ admin      |
| POST   | `/api/token/refresh/`        | Làm mới access token            | Chỉ admin      |

---

## 🔐 Xác thực người dùng (JWT)

Tạo tài khoản admin:

```bash
python manage.py createsuperuser
```

Đăng nhập để lấy token:

```http
POST /api/token/
Content-Type: application/json
{
  "username": "admin",
  "password": "yourpassword"
}
```

Gửi các request có quyền bằng:

```http
Authorization: Bearer <access_token>
```

---

## 🔍 Tìm kiếm phim

```http
GET /api/movies/?search=inception
```

---

## 💬 Gửi bình luận phim

```http
POST /api/movies/5/comments/
Content-Type: application/json

{
  "name": "Nguyễn Văn A",
  "content": "Phim rất hay, nên xem!"
}
```

---

## ⭐️ Gửi đánh giá phim (1 đến 5 sao)

```http
POST /api/movies/5/ratings/
Content-Type: application/json

{
  "score": 4
}
```

---

## 📂 Cấu trúc dự án

```
movie_site/
├── movies/
│   ├── models.py         # Movie, Comment, Rating
│   ├── serializers.py    # MovieSerializer, CommentSerializer, RatingSerializer
│   ├── views.py          # API cho phim, bình luận, đánh giá
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