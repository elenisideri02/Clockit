import os
 
 
class Settings:
    database_url: str = os.environ.get("DATABASE_URL", "postgresql://clockit:clockit@db:5432/clockit")
    jwt_secret: str = os.environ.get("JWT_SECRET", "clockit-dev-secret-change-in-prod")
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
 
 
settings = Settings()