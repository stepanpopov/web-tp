from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import F


class ProfileManager(models.Manager):
    def get_top5(self):
        return self.order_by('-rep')[:5]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='default.jpg')
    rep = models.IntegerField(default=0)

    manager = ProfileManager()

    def __str__(self):
        return f'({self.id}) {self.user.username}'


class TagManager(models.Manager):
    def get_top10(self):
        return self.annotate(count=Count('questions')).order_by('-count')[:10]

    def get_by_question(self, question):
        return self.filter(questions=question)

class Tag(models.Model):
    name = models.CharField(max_length=16)

    manager = TagManager()

    def __str__(self):
        return f'({self.id}) {self.name}'


class QuestionManager(models.Manager):
    def get_newest(self):
        return self.order_by('-creation_date')

    def get_top(self):
        return self.order_by('-rep')

    def get_by_tag(self, tag):
        return self.filter(tags=tag).order_by('-rep')

    def get_by_tag_name(self, tag_name):
        if Tag.manager.filter(name=tag_name).exists():    
            return self.filter(tags__name=tag_name).order_by('-rep')
        else:
            return None
    
    def get_by_id_or_None(self, id):
        questions_or_empty = self.filter(id=id)
        if not questions_or_empty.exists():
            return None
        else: return questions_or_empty[0]
    
class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')
    creation_date = models.DateTimeField(auto_now_add=True)
    rep = models.IntegerField(default=0)

    manager = QuestionManager()

    def __str__(self):
        return f'({self.id}) {self.profile.user.username}: {self.title}'


class AnswerManager(models.Manager):
    def get_by_question(self, q):
        return self.filter(question=q).order_by('-rep')

class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    # title = models.CharField(max_length=256)
    text = models.TextField()
    rep = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    manager = AnswerManager()

    def __str__(self):
        return f'({self.id}) {self.profile.user.username} commented question {self.question.title}'


class LikeToQuestionManager(models.Manager):
    def set_like(self, profile, question):
        if self.filter(profile=profile, question=question).exists():
            return None
        like = LikeToQuestion(profile=profile, question=question)
        like.save()
        Question.manager.filter(id=like.question.id).update(rep=F("rep")+1)
        Profile.manager.filter(id=like.profile.id).update(rep=F("rep")+1)
        return like


class LikeToQuestion(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_to_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    manager = LikeToQuestionManager()

    def __str__(self):
        return f'({self.id}) {self.profile.user.username} liked question {self.question.title}'


class LikeToAnswerManager(models.Manager):
    def set_like(self, profile, answer):
        if self.filter(profile=profile, answer=answer).exists():
            return None
        like = LikeToAnswer(profile=profile, answer=answer)
        like.save()
        Answer.manager.filter(id=like.answer.id).update(rep=F("rep")+1)
        Profile.manager.filter(id=like.profile.id).update(rep=F("rep")+1)
        return like

class LikeToAnswer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_to_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    manager = LikeToAnswerManager()

    def __str__(self):
        return f'({self.id}) {self.profile.user.username} liked answer by {self.answer.profile}'

