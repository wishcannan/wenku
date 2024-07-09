import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite:///example.db")

class Base(DeclarativeBase):
    pass

class Father1(Base):
    __tablename__ = "father"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(40),unique=True)
    age = Column(Integer)
    son1 = relationship('Son2')
    #son = relationship('Son')

class Son2(Base):
    __tablename__ = 'son'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(40),unique=True)
    age = Column(Integer)
    #father = relationship('Father')

    father_id = Column(Integer,ForeignKey('father.id'))

Base.metadata.create_all(engine)

MySession = sessionmaker(bind=engine)
session = MySession()
# f = Father1(name='ld',age=21)
# session.add(f)

# s1 = Son2(name='ww',age=1,father_id=1)
# s2 = Son2(name='wb',age=0,father_id=1)
# session.add_all([s1,s2])
# session.commit()

ret =session.query(Father1).filter_by(id=1).first()
print(ret)
for i in ret.son1:
    print(i.name,i.age)