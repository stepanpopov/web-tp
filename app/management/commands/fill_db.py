from django.core.management.base import BaseCommand
from app import models 
import random

class Command(BaseCommand):
    help = 'BD FILL'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='bd filling coefficient')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # user_names = ['user {}'.format(i) for i in range(ratio)]
        # users = [ models.User(username='user {}'.format(i)) for i in range(ratio)]
        # profiles = [models.Profile(user = users[i]) for i in range(ratio)]
        users = []
        profiles = []
        questions = []
        answers = []
        for i in range(ratio):
            users.append(models.User(username='user {}'.format(i)))
            profiles.append(models.Profile(user = users[i]))
            questions_to_save = []
            for j in range(10):
                questions_to_save.append(models.Question(profile=profiles[i], title = "HOW{}?".format(10*i + j)))
                questions.append(questions_to_save[j])
                answers_to_save = []
                for k in range(10):
                    answers_to_save.append(models.Answer(profile=random.choice(profiles), question = questions[10*i + j], text = "DO DO DO" ))
                    answers.append(answers_to_save[k])
                models.Answer.manager.bulk_create(answers_to_save)
            models.Question.manager.bulk_create(questions)

        models.User.objects.bulk_create(profiles)
        models.Profile.manager.bulk_create(profiles)

        tags = [models.Tag(name="tag{}".format(i)) for i in range(ratio)]
        models.Tag.manager.bulk_create(tags)

        questions_to_tags = [models.Question.tags.through(question_id=random.choice(questions).id, tag_id=random.choice(tags).id) for i in range(ratio)]
        models.Question.tags.through.objects.bulk_create(questions_to_tags)

        self.stdout.write("ONLY LIKES REMAINS\n")

        for i in range(ratio):
            liked_questions_indxs = random.sample(range(len(questions)), 100)
            liked_answers_indxs = random.sample(range(len(answers)), 100)

            likes_to_q_to_save = []
            for ind in liked_questions_indxs:
                likes_to_q_to_save.append(models.LikeToQuestion(profile=profiles[i], question=questions[ind]))
                questions[ind].rep+=1
            models.LikeToQuestion.objects.bulk_create(likes_to_q_to_save)

            likes_to_a_to_save = []
            for ind in liked_answers_indxs:
                likes_to_a_to_save.append(models.LikeToAnswer(profile=profiles[i], answer=answers[ind]))
                answers[ind].rep+=1
            models.LikeToAnswer.objects.bulk_create(likes_to_a_to_save)
            
        models.Question.manager.bulk_update(questions, ['rep'])
        models.Answer.manager.bulk_update(answers, ['rep'])
            
        
        # TODO BEST USERS


        self.stdout.write("DONE")