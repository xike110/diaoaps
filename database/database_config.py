from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# 壮大运数据库配置信息
ZHUANGDAYUN_DB_CONFIG = {
    'host': 'rm-uf64s1hanx2bcg96i4o.mysql.rds.aliyuncs.com',
    'port': 3306,
    'username': 'xiaoyun1',
    'password': 'Xiaoyun_123456',
    'database': 'zhuangdayun',
    'charset': 'utf8mb4'
}

# 微信数据库配置信息
WECHAT_DB_CONFIG = {
    'host': 'rm-uf64s1hanx2bcg96i4o.mysql.rds.aliyuncs.com',
    'port': 3306,
    'username': 'xiaoyun1',
    'password': 'Xiaoyun_123456',
    'database': 'wechat',
    'charset': 'utf8mb4'
}

# 创建壮大运数据库连接字符串
ZHUANGDAYUN_DATABASE_URL = f"mysql+pymysql://{ZHUANGDAYUN_DB_CONFIG['username']}:{ZHUANGDAYUN_DB_CONFIG['password']}@{ZHUANGDAYUN_DB_CONFIG['host']}:{ZHUANGDAYUN_DB_CONFIG['port']}/{ZHUANGDAYUN_DB_CONFIG['database']}?charset={ZHUANGDAYUN_DB_CONFIG['charset']}"

# 创建微信数据库连接字符串
WECHAT_DATABASE_URL = f"mysql+pymysql://{WECHAT_DB_CONFIG['username']}:{WECHAT_DB_CONFIG['password']}@{WECHAT_DB_CONFIG['host']}:{WECHAT_DB_CONFIG['port']}/{WECHAT_DB_CONFIG['database']}?charset={WECHAT_DB_CONFIG['charset']}"

# 创建壮大运数据库引擎
zhuangdayun_engine = create_engine(
    ZHUANGDAYUN_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # 设置为True可以打印SQL语句
)

# 创建微信数据库引擎
wechat_engine = create_engine(
    WECHAT_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # 设置为True可以打印SQL语句
)

# 创建壮大运数据库会话工厂
ZhuangDaYunSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=zhuangdayun_engine)

# 创建微信数据库会话工厂
WechatSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=wechat_engine)

# 获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建数据库会话（同步方式）
def create_db_session():
    """创建数据库会话（同步方式）"""
    return SessionLocal()