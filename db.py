from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class habr_news(Base):
    __tablename__ = "habr_news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    upvotes = Column(String)
    downvotes = Column(String)
    text = Column(String)
    date = Column(String)


Base.metadata.create_all(bind=engine)
