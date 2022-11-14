from django.db import models

QUESTIONS = [
    {
        'id' : id,
        'answers_num' : id,
        'tags': ['meaning_of_life', 'c++'],
        'text': 'Lorem ' * id * id * id * id,
        'title': 'question {}'.format(id),
        'user': 'stepapopov',
        'rep' : id
    } for id in range(1, 6)
]

HOT_QUESTIONS = sorted(QUESTIONS, key=lambda x: x['answers_num'], reverse=True)

ANSWERS = { 
    question['id'] : [ 
        {
            'id' : (id + 1),
            'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolor ea, expedita hic magnam officia qui quod sed soluta suscipit vitae.',
            'title': 'answer {}'.format(id + 1),
            'user': 'yarikTri',
            'rep' : (id + 1)
        } for id in range(question['answers_num'])
    ] for question in QUESTIONS 
} 

tags_temp = {}
for question in QUESTIONS:
    for tag in question['tags']:
        if tag in tags_temp:
            tags_temp[tag] += 1
        else:
            tags_temp.update({tag : 0})
TAGS = [
    {
        'tag_title' : tag,
        'question_num' : question_num
    } for tag, question_num in tags_temp.items()
]

POPULAR_TAGS = sorted(TAGS, key=lambda x: x['question_num'], reverse=True)[:20]


USERS = [
    {
        'name' : 'stepanpopov',
        'question_num' : 6,
        'rep' : 10000 
    },
    {
        'name' : 'yarikTri',
        'question_num' : 0,
        'rep' : 500
    }
]

POPULAR_USERS = sorted(USERS, key=lambda x: x['rep'], reverse=True)[:10]
