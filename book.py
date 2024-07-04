from sqlalchemy.orm import Mapped, mapped_column
import database
import sqlalchemy
import datetime
class Wenkubook1(database.OrmBase):
    __tablename__ = 'book'
    #主键
    uid: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True,autoincrement=True,)  # 创建表后最好手动改成unsigned
    #bookid
    book_id:Mapped[int] = mapped_column(sqlalchemy.Integer)
    #书名很重要
    book_name:Mapped[str] = mapped_column(sqlalchemy.String(100))
    #如果换做以前 可能会设置 书->章->节 节点里面单独存放 图片 或者图片的形式 想起有些小说节里面又有图片 又有文字
    #忘记当时怎么处理的了
    chapter_id:Mapped[int] = mapped_column(sqlalchemy.Integer)
    #chapter_name
    chapter_name:Mapped[str] = mapped_column(sqlalchemy.String(100))
    #现在直接存long_text
    chapter_text:Mapped[str] = mapped_column(sqlalchemy.TEXT)
    update_time: Mapped[datetime.datetime] = mapped_column(sqlalchemy.DateTime,default=datetime.datetime.now())

    def __repr__(self):
        return f'chapter_name:{self.chapter_name},chapter_text:{self.chapter_text}'#为什么不打印update_time 因为只有插入时会带上

def insert(bookid:int=0,bookname:str='',chapterid:int=0,chaptername:str='',chaptertext:str=''):
    with database.get_session() as session:
        # session.configure()
        session.begin()
        book = Wenkubook1(
            book_id = bookid,
            book_name = bookname,
            chapter_id=chapterid,
            chapter_name = chaptername,
            chapter_text = chaptertext,
        )
        session.add(book)
        session.commit()


def get_book(aid:int=0,cid:int=0) ->Wenkubook1:
    with database.get_session() as session:
        u1 = session.scalars(
            sqlalchemy.select(Wenkubook1).filter(
                Wenkubook1.book_id == aid and Wenkubook1.chapter_id == cid
            )
        ).one_or_none()
        if u1:
            return u1
    return None

# database.init()
# insert()
# print(get_book(2,2))





