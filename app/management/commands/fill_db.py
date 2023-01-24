from django.core.management.base import BaseCommand
from app import models 
from django.db.models import F
import random

class Command(BaseCommand):
    help = 'BD FILL'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='bd filling coefficient')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        users = [models.User(username='user {}'.format(i)) for i in range(ratio)]
        users = models.User.objects.bulk_create(users)
        self.stdout.write("USERS FILLED\n")

        profiles = [models.Profile(user = users[i]) for i in range(ratio)]
        profiles = models.Profile.manager.bulk_create(profiles)
        self.stdout.write("PROFILES FILLED\n")


        questions = [models.Question(profile=profiles[i], 
                                     title = "HOW{}?".format(10*i + j),
                                     text = "HOW HOW HOW HOW") 
                                     for i in range(ratio) 
                                        for j in range(10)]
        questions = models.Question.manager.bulk_create(questions)
        self.stdout.write("QUESTIONS FILLED\n")


        answers = [models.Answer(profile=random.choice(profiles), 
                                 question = random.choice(questions), 
                                 text = "DO DO DO" ) 
                                 for i in range(ratio * 100)]
        answers = models.Answer.manager.bulk_create(answers)
        self.stdout.write("ANSWERS FILLED\n")


        tags = [models.Tag(name="tag{}".format(i)) for i in range(ratio)]
        tags = models.Tag.manager.bulk_create(tags)
        self.stdout.write("TAGS FILLED\n")

        #questions_to_tags = [models.Question.tags.through(question_id=random.choice(questions).id, 
                                                          #tag_id=random.choice(tags).id) 
                                                          #for i in range(ratio)]
        questions_to_tags = []
        for i in range(ratio):
            questions_indxs = random.sample(range(len(questions)), 10)
            for ind in questions_indxs:
                questions_to_tags.append(models.Question.tags.through(question_id=questions[ind].id, 
                                                         tag_id=tags[i].id))

        questions_to_tags = models.Question.tags.through.objects.bulk_create(questions_to_tags)
        self.stdout.write("TAGS ATTACHED TO QUESTIONS\n")

        
        self.stdout.write("ONLY LIKES REMAINS\n")


        likes_to_q = []
        likes_to_a = []
        for i in range(ratio):
            liked_questions_indxs = random.sample(range(len(questions)), 100)
            liked_answers_indxs = random.sample(range(len(answers)), 100)

            for ind in liked_questions_indxs:
                likes_to_q.append(models.LikeToQuestion(profile=profiles[i], question=questions[ind]))
                questions[ind].rep+=1
            
            for ind in liked_answers_indxs:
                likes_to_a.append(models.LikeToAnswer(profile=profiles[i], answer=answers[ind]))
                answers[ind].rep+=1
            

        models.LikeToQuestion.manager.bulk_create(likes_to_q)
        models.LikeToAnswer.manager.bulk_create(likes_to_a)
        # models.Question.manager.bulk_update(questions, ['rep'])
        # models.Answer.manager.bulk_update(answers, ['rep'])
        self.stdout.write("LIKES FILLED\n")
            

        self.stdout.write("DONE")
        