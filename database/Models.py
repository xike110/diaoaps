"""
数据库模型文件
使用SQLite数据库 + SQLAlchemy ORM
"""
import os
import datetime
import contextlib
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# 数据库连接
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
# 2. 创建引擎
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},  # 仅SQLite需要，允许多线程访问
    echo=False,  # 显示SQL语句
    # pool_size=5,  # 连接池大小
    # max_overflow=10,  # 最大溢出连接数
    # pool_timeout=30,  # 获取连接超时时间(秒)
    # pool_recycle=3600  # 连接回收时间(秒)
)

# 创建会话
Session = sessionmaker(
    bind=engine,  # 创建会话
    # autocommit=False,  # 关闭自动提交
    # autoflush=False,  # 关闭自动刷新
)
session = Session()

# 创建基类
Base = declarative_base()


# 会话管理上下文，自动处理提交、回滚和关闭
@contextlib.contextmanager
def session_scope():
    """提供事务范围的会话对象。
    自动处理提交或回滚事务并关闭会话。
    使用方式:
    with session_scope() as session:
        session.add(some_object)
        session.add(some_other_object)
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"数据库操作出错，已回滚: {str(e)}")
        raise
    finally:
        session.close()


class App(Base):
    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='应用ID主键')
    name = Column(String(100), nullable=False, comment='应用名称')
    belongs = Column(Boolean, default=False, comment='应用归属')  # True=系统归属 False=客户添加
    category = Column(String(50), nullable=False, comment='应用分类')
    description = Column(Text, nullable=True, comment='应用描述')
    icon = Column(String(255), nullable=True, comment='应用图标路径')
    bgcolor = Column(String(50), default='#e6f7ff', comment='应用背景颜色')
    type = Column(String(50), nullable=False, comment='应用类型')  # 应用类型 builtin = 应用软件, external = 外部软件 link = 链接
    open = Column(String(1024), nullable=False, comment='打开命令或路径')  # 应用软件路径="WebMain.main_str" 外部软件路径="C:\Windows\System32\calc.exe" 链接="https://www.pptink.com"
    recommend = Column(Boolean, default=False, comment='是否推荐')
    isview = Column(Boolean, default=True, comment='是否可见')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


# 系统设置表
class SystemSetting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='设置ID主键')
    key = Column(String(50), unique=True, nullable=False, comment='设置键名')
    value = Column(Text, nullable=True, comment='设置值')
    description = Column(Text, nullable=True, comment='设置描述')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


# 开启启动应用表
class StartupApp(Base):
    __tablename__ = 'startup'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='启动项ID主键')
    guiname = Column(String(255), nullable=False, comment='应用名称')
    sign = Column(String(255), nullable=False, comment='应用标识')
    main = Column(String(255), nullable=False, comment='应用入口')
    menuname = Column(String(255), nullable=False, comment='菜单名称')
    formdata = Column(JSON, nullable=True, comment='应用参数存储json')
    enabled = Column(Boolean, default=True, comment='是否启用')
    bkgrdstat = Column(Boolean, default=False, comment='后台运行')
    autoclose = Column(Boolean, default=False, comment='结束关闭')
    priority = Column(Integer, default=0, comment='启动优先级')
    delay = Column(Integer, default=0, comment='启动延迟（秒）')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


# 定时启动应用表
class TimedApp(Base):
    """
    # 定时任务数据库
    # 定时类型
    # {
    #     "间隔(天)": "days",
    #     "间隔(小时)": "hours",
    #     "间隔(分钟)": "minutes",
    #     "间隔(秒)": "seconds",
    #     "每天几点": "daily",
    #     "自定义": "custom"
    # }
    """
    __tablename__ = 'timed'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='定时项ID主键')
    guiname = Column(String(255), nullable=False, comment='应用名称')
    sign = Column(String(255), nullable=False, comment='应用标识')
    main = Column(String(255), nullable=False, comment='应用入口')
    menuname = Column(String(255), nullable=False, comment='菜单名称')
    timedtype = Column(String(50), nullable=True, default=None, comment='定时类型')
    timedvalue = Column(String(50), nullable=True, default=None, comment='定时值')
    formdata = Column(JSON, nullable=True, comment='应用参数存储json')
    enabled = Column(Boolean, default=True, comment='是否启用')
    bkgrdstat = Column(Boolean, default=False, comment='后台运行')
    autoclose = Column(Boolean, default=True, comment='结束关闭')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


# 命主分组表
class BirthGroup(Base):
    __tablename__ = 'birth_groups'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='分组ID')
    name = Column(String(255), nullable=False, unique=True, default="未分组", comment='分组名称')
    description = Column(Text, nullable=True, comment='分组描述')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

    # 定义关系
    births = relationship("birthtime", back_populates="group_info", cascade="all, delete-orphan")


#  用户生辰库
class birthtime(Base):
    __tablename__ = 'birth'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    usid = Column(String(255), nullable=False, comment='用户ID')  # 唯一性ID
    group_id = Column(Integer, ForeignKey('birth_groups.id', ondelete='CASCADE'), nullable=False, comment='分组ID')
    name = Column(String(255), nullable=False, comment='姓名')
    sex = Column(String(255), nullable=False, comment='性别')
    five = Column(String(255), nullable=False, comment='五行')
    birthtime = Column(String(255), nullable=False, comment='八字时辰')
    solarcal = Column(String(255), nullable=False, comment='公历生日')
    lunarcal = Column(String(255), nullable=False, comment='农历生日')
    birthdata = Column(JSON, nullable=True, comment='命主排盘json')
    notes = Column(Text, nullable=True, comment='备注')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    # 定义关系
    userinfos = relationship("UserInfo", back_populates="birth", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="birth", cascade="all, delete-orphan")
    group_info = relationship("BirthGroup", back_populates="births")


# 命主信息表-动态扩展字段
class UserInfo(Base):
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    birth_id = Column(Integer, ForeignKey('birth.id', ondelete='CASCADE'), nullable=False, comment='命主ID')
    name = Column(String(255), nullable=False, comment='字段名称')
    value = Column(Text, nullable=True, comment='字段值')
    notes = Column(Text, nullable=True, comment='批注')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

    # 定义关系
    birth = relationship("birthtime", back_populates="userinfos")


# 命主分析表-动态扩展字段
class Analysis(Base):
    __tablename__ = 'analysis'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    birth_id = Column(Integer, ForeignKey('birth.id', ondelete='CASCADE'), nullable=False, comment='命主ID')
    name = Column(String(255), nullable=False, comment='字段名称')
    value = Column(Text, nullable=True, comment='字段值')
    notes = Column(Text, nullable=True, comment='批注')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

    # 定义关系
    birth = relationship("birthtime", back_populates="analyses")


class Sendmsg(Base):
    __tablename__ = 'sendmsg'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    channel = Column(String(255), nullable=False, default='抖店', comment='渠道')
    shop_id = Column(String(255), nullable=False, comment='店铺ID')
    pigeon_cid = Column(String(255), nullable=False, comment='鸽子ID')
    message = Column(JSON, comment='消息实体')
    is_delete = Column(Boolean, default=False, comment='是否删除')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


# 创建所有表
def init_db():
    Base.metadata.create_all(engine)  # 创建所有表
    # 初始化默认命主分组数据
    with session_scope() as sessions:
        # 检查是否已存在默认分组
        if not sessions.query(BirthGroup).first():
            # 创建默认分组数据
            default_groups = [
                BirthGroup(id=1, name='未分组', description='默认分组'),
                BirthGroup(id=2, name='常用', description='常用排盘'),
                BirthGroup(id=3, name='亲属', description='旁系亲属'),
                BirthGroup(id=4, name='同事', description='工作关系'),
                BirthGroup(id=5, name='客户', description='商业关系'),
                BirthGroup(id=6, name='名人', description='名人排盘'),
                BirthGroup(id=7, name='直系', description='直系亲属'),
                BirthGroup(id=8, name='朋友', description='朋友关系'),
                BirthGroup(id=9, name='同学', description='同学关系'),
            ]
            sessions.add_all(default_groups)


if __name__ == "__main__":
    init_db()
