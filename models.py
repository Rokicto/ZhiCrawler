from peewee import *
"""
In order to store answers, database should be MySQL and MySQL only. See http://peewee.readthedocs.org/en/latest/peewee/models.html#field-types-table 
for more information.
"""

db = MySQLDatabase("ZhiCrawler", user="ZhiCrawler", charset="utf8mb4")

class BaseModel(Model):
    class Meta:
        database = db
        

class _Topic(BaseModel):
    id = IntegerField(primary_key=True)
    depth = IntegerField(default=None, null=True)


class _TopicRelation(BaseModel):
    parent = IntegerField()
    child = IntegerField()
    

class Topic:
    pass
    

class Question(BaseModel):
    id = IntegerField(primary_key=True)


class User(BaseModel):
    id = IntegerField(primary_key=True)
    nickname = CharField()


class Answer(BaseModel):
    question = ForeignKeyField(Question)
    author = ForeignKeyField(User)
    content = TextField()

    
def setup():
    pass
