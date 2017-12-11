from mongoengine import *
import datetime

connect('monoengine_test',host='localhost',port=27017)

# class Post(Document):
#     title=StringField(required=True,max_length=200)
#     content=StringField(required=True)
#     author=StringField(required=True)
#     published=DateTimeField(default=datetime.datetime.now)
# class Post_doc(Document):
#     url=StringField(required=True,unique=True)
#     content=StringField(required=True)
class Post_fileContxt(Document):
    url=StringField(required=True,unique=True)
    content=StringField(required=True)
def contentToFile(url,content):
    try:
        post=Post_fileContxt(url,content)
        post.save()
    except:
        print(url)

#post2=Post_doc(url='127.0.0.1',content='djifjdi')
# post3=Post_doc(url='url1',content='url1-content')
# post4=Post_doc(url='url2',content='url2-content')
# post5=Post_doc(url='url3',content='url3-content')
# post1=Post(
#     title='Sample Post',
#     content='Some engaging content',
#     author='Scott'
# )
#post2.save()
# post3.save()
# post4.save()
# post5.save()
#print(post2.url)
for post in Post_fileContxt.objects:
    print('url'+post.url)
    print('content'+post.content)
    #print('content'+post.content.strip())
# doc2=Post_doc.objects(url='url1')
# for post in doc2:
#     print(post.content)
# print(doc2.content)
# post1.title='A Better Post Title'
# post1.save()
# print(post1.title)
# post3=Post_doc(
#     url='127.0.0.1',
#     content='djifjdifdf'
# )
# post3.save()

# print(post3.url)