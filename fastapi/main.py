import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# 환경 변수에서 데이터베이스 URL 가져오기 (기본값 설정)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://moon:1234@postgres:5432/moon")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"데이터베이스 연결 오류: {e}")
    raise

# 의존성 함수: 데이터베이스 세션 생성 및 관리
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    # 여기서 db 세션을 사용하여 데이터베이스 작업을 수행할 수 있습니다.
    return {"item_id": item_id}

# 데이터베이스 모델 예시 (실제 사용시 구현 필요)
# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String, index=True)

# 애플리케이션 시작시 데이터베이스 테이블 생성 (필요한 경우)
# @app.on_event("startup")
# async def startup():
#     Base.metadata.create_all(bind=engine)
