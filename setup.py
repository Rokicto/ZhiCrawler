from distutils.core import setup

setup(
    name="ZhiCrawler",
    version="0.1.0",
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'peewee',
        'pymysql',
    ],
)