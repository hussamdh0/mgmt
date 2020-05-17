from django.contrib.auth.models import AbstractUser
from django.db import models

NN = {'null': True, 'blank': True}
NNN = {**NN, 'default': None}
NNE = {**NN, 'default': ''}
ML = {'max_length': 1500, }
FKOD = {'on_delete': models.SET_NULL, }
CNNN = {**ML, **NNN}
CNNE = {**ML, **NNE}
FKKW = {**FKOD, **NNN}
CF = models.CharField
TF = models.TextField
BF = models.BooleanField
UF = models.URLField
IF = models.IntegerField
FK = models.ForeignKey

MDL = models.Model

def text(s=''):
    if len(s)>0: return models.CharField(s, **CNNE)
    else: return models.CharField(**CNNE)


def long_text(s=''):
    if len(s)>0: return models.TextField(s, **NNE)
    else: return models.TextField(**NNE)


class BaseModel(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255, unique=False, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=True, editable=False)
    
    def __str__(self):
        return str(self.name)
    
    @property
    def timestamp_str(self):
        return self.creation_date.strftime("%B %d, %Y")
    
    class Meta:
        abstract = True


class BaseUserModel(AbstractUser):
    def __str__(self):
        return str(self.username)
    
    class Meta:
        abstract = True


class SingletonManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        if qs.count() == 0:
            super(SingletonManager, self).create(pk=1)
            qs = super().get_queryset()
        return qs
    

class Singleton(MDL):
    objects = SingletonManager
    @classmethod
    def object(cls):
        return cls._default_manager.all().first()  # Since only one item
    
    def save(self, *args, **kwargs):
        if self.id == 1:
            return super().save(*args, **kwargs)
        return
    
    def delete(self, using=None, keep_parents=False):
        return
    
    class Meta:
        abstract = True


class HasOrdering(MDL):
    ordering = IF(**NNN)
    
    class Meta:
        ordering = ['ordering', ]
        abstract = True


class AbstractArticle(BaseModel):
    title = models.CharField(max_length=255, unique=False, null=True, blank=True)
    text = models.TextField(unique=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    align_right = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.title)
    
    @property
    def style(self):
        return 'style=text-align:right' if self.align_right else ''
    
    class Meta:
        abstract = True
