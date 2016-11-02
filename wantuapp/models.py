from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT

Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://zhang:zhang@172.16.5.15/fasttrave?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WanTuEntity(Base):
    __tablename__ = 'j_viewspot_wantu'

    viewspotid = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    product_id = Column(String(255))
    # city_code = Column(String(255))
    # supplier_id = Column(String(255))
    # model = Column(String(255))
    # type = Column(String(255))
    status = Column(String(255))
    # source_url = Column(String(255))
    # date_added = Column(String(255))
    # date_modified = Column(String(255))
    # description = Column(String(255))
    # buy_label = Column(String(255))

    # 价格信息
    # orig_price = Column(String(255))
    price = Column(String(255))
    price_title = Column(String(255))
    # mark_price = Column(String(255))
    # discount_rule = Column(String(255))
    jsoninfo = Column(LONGTEXT)

    # 外键信息
    img = relationship('WangTuImgEntity')


class WangTuImgEntity(Base):
    __tablename__ = 'j_viewspot_wantu_img'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))

    # 外键信息
    viewspotid = Column(Integer, ForeignKey('j_viewspot_wantu.viewspotid'))


# 初始化表
def init_db():
    Base.metadata.create_all(engine)
    print('数据库初始化成功...')
