from sqlalchemy.orm import Mapped, mapped_column,relationship,subqueryload,joinedload,lazyload
from sqlalchemy import Integer, String,DateTime,select,ForeignKey,Text,update
import database
from datetime import datetime
from typing import List,Union
class Wenkubook1(database.OrmBase):
    __tablename__ = 'book'
    #主键
    uid: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True,)  # 创建表后最好手动改成unsigned
    #bookid
    book_id:Mapped[int] = mapped_column(Integer)
    #书名很重要
    book_name:Mapped[str] = mapped_column(String(100))
    # son_chapter = relationship('Wenkubook2',lazy="selectin")#要大写 这里填写类名
    son_chapter = relationship('Wenkubook2')#要大写 这里填写类名
    '''
    lazy mode:
    select - (默认) 后台会用select语句一次性加载所有数据，即访问到属性的时候，就会全部加载该属性的数据
    selectin 可通过 或 选项获得，这种加载形式会发出第二个（或多个）SELECT 语句，该语句 将父对象的主键标识符组合到 IN 子句中， 以便一次加载相关集合/标量引用的所有成员 按主键。Select IN 加载详见 Select IN loading。lazy='selectin'
    joined 可通过 或 选项使用，此加载形式将 JOIN 应用于给定的 SELECT 语句 以便将相关行加载到同一结果集中。加入急切加载 详见 Joined Eager Loading。lazy='joined'
    raise loading
    subquery loading
    write only loading 
    dynamic loading 
    '''
    update_time: Mapped[datetime] = mapped_column(DateTime,default=datetime.now())

    def __repr__(self):
        return f'book_id:{self.book_id},book_name:{self.book_name}'#为什么不打印update_time 因为只有插入时会带上
    
class Wenkubook2(database.OrmBase):
    __tablename__ = 'chapter'
    chapter_id:Mapped[int] = mapped_column(Integer,primary_key=True)
    chapter_name:Mapped[str] = mapped_column(String(100))
    book_id = mapped_column(Integer,ForeignKey('book.book_id'))
    def __repr__(self):
        return f'chapter_id:{self.chapter_id},book_name:{self.chapter_name},book_id:{self.book_id}'
    
class Wenkubook3(database.OrmBase):
    __tablename__ = 'chaptertext'
    chapter_id:Mapped[int] = mapped_column(Integer,primary_key=True)
    bid:Mapped[int] = mapped_column(Integer)
    chapter_name:Mapped[str] = mapped_column(String(100))
    chapter_text:Mapped[str] = mapped_column(Text)
    chapter_order:Mapped[int] = mapped_column(Integer)
    def __repr__(self):
        return f'book_id:{self.chapter_id},book_name:{self.chapter_name},chapter_order:{self.chapter_order}'
    


def insert(book:Wenkubook1,chapter:List[Wenkubook2]) ->bool:
    #不检查chapter里面book_id是否相统一 是否有点不好
    with database.get_session() as session:
        # 要成功一起成功 要失败一起失败
        try:
            session.begin()
            if book:
                session.add(book)
            if chapter:
                session.add_all(chapter)
            session.commit()
        except Exception as e:
            #报错就回滚
            session.rollback()
            print(e)
        finally:
            session.close()

def insertbooktext(book:Wenkubook3) ->bool:
    with database.get_session() as session:
        # 要成功一起成功 要失败一起失败
        try:
            session.begin()
            if book:
                session.add(book)
            session.commit()
        except Exception as e:
            #报错就回滚
            session.rollback()
            print(e)
        finally:
            session.close()




def get_book(aid:int=0,cid:int=0) ->Union[Wenkubook1,Wenkubook2]:
    with database.get_session() as session:
        if aid and cid:
            stmt  = select(Wenkubook2).filter(
                Wenkubook2.book_id == aid and Wenkubook2.chapter_id == cid
            )
        else:
            #如果使用外键 只是这样查询 不会有n+1的情况
            stmt  = select(Wenkubook1).filter(
                Wenkubook1.book_id == aid 
            )
            # sql = select(Wenkubook1).options(selectinload(Wenkubook2)).filter(Wenkubook1.book_id == aid)
        u1 = session.scalars(
            stmt 
        )
        if u1:
            return u1.first()
    return None


def update_order(aid:int=0,cid:int=0,ord:int=0):

database.init()
# a = Wenkubook1(book_id=2,book_name='测试2')
# b1 = Wenkubook2(chapter_id=1,chapter_name='章节1',book_id= 1)
# b2 = Wenkubook2(chapter_id=2,chapter_name='章节2',book_id= 1)
# insert(a,[])


# c = get_book(3271)
# for i in c.son_chapter:
#     print(i)

#子查询
# with database.get_session() as session:
#     # stmt = select(Wenkubook1).options(
#     #     subqueryload(Wenkubook1.son_chapter)
#     # ).filter(
#     #     Wenkubook1.book_id == 3271
#     # )
#     stmt = select(Wenkubook1).options(
#         # joinedload(Wenkubook1.son_chapter)
#         subqueryload(Wenkubook1.son_chapter.and_(Wenkubook2.chapter_id > 135479))
#     ).filter(
#         Wenkubook1.book_id == 3271
#     )
#     print(stmt)
#     u1 = session.scalars(
#         stmt 
#     )
#     c = u1.first()
#     print(c)
#     if c.son_chapter:
#         print(c.son_chapter)




