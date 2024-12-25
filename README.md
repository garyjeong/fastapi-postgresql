# fastapi-postgresql
SQLAlchemy + Alembic을 이용한 PostgreSQL ORM 구성

---
## Local PostgreSQL Docker Setup
```bash
docker build -t local-postgres .
docker run -d --name local-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 local-postgres:latest
```

---
## alembic 초기 설정 명령어

```bash
alembic init migrations
```

---
## alembic 버전 생성 명령어
```bash
ENV={local|production} alembic revision --rev-id "{revision id}" --autogenerate -m "{migration message}"
ENV={local|production} alembic upgrade head
```