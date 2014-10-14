import datetime

from peewee import *
from app import db



class UnknownFieldType(object):
    pass


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    category_id = PrimaryKeyField(db_column='category_id')
    category_name = CharField()

    class Meta:
        db_table = 'category'


class Role(BaseModel):
    class Meta:
        db_table = 'role'
        
    role_id = PrimaryKeyField()
    level = IntegerField(default=40)
    role = CharField(null=False)


class User(BaseModel):
    user_id = PrimaryKeyField(db_column='user_id')
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    mail = CharField(null=False, unique=True)
    nickname = CharField()
    user_password = CharField()
    picture = CharField(null=True)
    role = ForeignKeyField(db_column='role_id', rel_model=Role)

    @staticmethod
    def encode_password(password):
        import hashlib
        m = hashlib.md5()
        m.update(password)
        return m.hexdigest()

    class Meta:
        db_table = 'user'


class Post(BaseModel):
    post_id = PrimaryKeyField(db_column='post_id')
    category = ForeignKeyField(db_column='category_id', rel_model=Category)
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    date_posted = DateTimeField(default=datetime.datetime.now())
    date_updated = DateTimeField(default=datetime.datetime.now())

    post_text = CharField(null=True)
    title = CharField(null=True)

    likes = IntegerField(default=0)
    views = IntegerField(default=0)

    draft = BooleanField()
    deleted = BooleanField()

    @property
    def comments(self):
        """
        Get comments count
        """
        return 10

    class Meta:
        db_table = 'post'


    @classmethod
    def get_drafts(cls):
        """
        Return only draft posts
        """
        return cls.select().where(Post.deleted == False,
                                  Post.draft == True)

    @classmethod
    def get_deleted(cls):
        """
        Return only deleted
        """
        return cls.select().where(Post.deleted == True)

    @classmethod
    def get_posts(cls):
        """
        Get not deleted and not drafts to display in post list
        """
        return cls.select().where(Post.deleted == False,
                                  Post.draft == False)

    @classmethod
    def get_for_user(cls, user_id):
        """
        Get published posts for this specific user
        """
        return cls.select().where(Post.deleted == False,
                                  Post.draft == False,
                                  Post.user == user_id)

    def get_all(self):
        raise NotImplemented


class Photo(BaseModel):
    class Meta:
        db_table = 'photo'

    photo_id = PrimaryKeyField(db_column='photo_id')
    photo = CharField()
    desc = CharField()
    date_added = DateTimeField(default=datetime.datetime.now)


class Banner(BaseModel):
    class Meta:
        db_table = 'banner'

    banner_id = PrimaryKeyField(db_column='banner_id')
    desc = CharField()
    link = CharField()
    img = CharField()


class Quote(BaseModel):
    class Meta:
        db_table = 'quote'

    quote_id = PrimaryKeyField(db_column='quote_id')
    text = CharField(null=False)
    author = CharField(null=False)


class Tag(BaseModel):
    tag_id = PrimaryKeyField(db_column='tag_id')
    text = CharField(null=False, unique=True)

    class Meta:
        db_table = 'tag'


class Tag_to_Post(BaseModel):
    post_id = ForeignKeyField(db_column='post_id', rel_model=Post)
    tag_id = ForeignKeyField(db_column='tag_id', rel_model=Tag)

    class Meta:
        db_table = 'tag_to_post'

