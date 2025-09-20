# 📝 Minimal Blog API

A simple yet production-style Blog API built with Django REST Framework.  
Implements **PostgreSQL**, **Redis caching**, **JWT auth**, and **drf-spectacular** for clean documentation.

---

## 🚀 Features

- 👤 **Custom User** (phone-based login) + Profile (bio, avatar, location, website)
- 🔑 **JWT Authentication** (access/refresh)
- 📝 **Posts** with categories, rich text, slug, description, reading time
- ❤️ **Likes/Dislikes** + comments (with report system)
- 👥 **Follow / Unfollow** users
- 🚫 **Block users**
- 🔍 **Search & Ordering** (title, description, updated_at, …)
- 📊 **Counts** (comments_count, likes_count) with annotate
- 📦 **Redis caching** for heavy endpoints (post list, category posts)
- 📑 **OpenAPI Schema** + Swagger & Redoc UI
- 🧪 **Postman Collection** ready for testing
- ⚙️ **Docker support coming soon...!**

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Auth**: JWT (SimpleJWT)
- **Docs**: drf-spectacular (Swagger & Redoc)

---

## ⚡ Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/amir-pashayi/minimal-blog-api.git
cd minimal-blog-api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup .env
Create a `.env` file (you can copy from `.env.example`):

```env
SECRET_KEY=your-secret
DEBUG=True
POSTGRES_DB=minimal_blog
POSTGRES_USER=mb_username
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/1
```

### 3. Migrate & Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Server
```bash
python manage.py runserver
```

---

## 📚 API Documentation

After running the server:

- Swagger UI → [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- Redoc → [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

OpenAPI schema files are also available:
- `docs/openapi.json`
- `docs/openapi.yaml`

---

## 🧪 Postman Collection

For quick testing:

- [postman_collection.json](./postman_collection.json)  
- [postman_environment.json](./postman_environment.json)

📌 Steps:
1. Import collection and environment in Postman  
2. Login → set `access` token in env  
3. Test away 🎯

---

## 🗂️ Project Structure

```
minimal-blog-api/
├── accounts/     # User, Profile, Follow, Block
├── posts/        # Posts, Categories, Likes
├── comments/     # Comments, Reports
├── blog/         # settings, urls, utils
├── docs/         # OpenAPI JSON/YAML
└── ...
```

---

## ❤️ Credits

Developed with ❤️ by **Amir Pashayi**
