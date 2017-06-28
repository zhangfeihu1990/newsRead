# -*- encoding:UTF-8 -*-
from mongoalchemy.document import Document
from mongoalchemy.fields import *

class News(Document):
     title =  StringField()
     update_time = StringField()
     author = StringField()
     content = StringField()
     #url = StringField()
     #site = StringField()
     #adding_tme =