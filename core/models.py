from .abstract import *
from django.contrib import admin


class User(BaseUserModel):
    @property
    def name(self):
        res = f'{self.first_name} {self.last_name}'
        if res is None or res == ' ':
            return self.username
        return res


person_texts = ['text1', 'text2']
person_long_texts = ['long_text1', 'long_text2']


e = type('Person', (BaseModel,), {
    'first_name': CF('first_name', **CNNE),
#    'last_name': CF('last_name', **CNNE),'__module__': __name__,
    '__module__': __name__,
})
admin.site.register(e)


class Test(BaseModel):
    texts = ['text1', 'text2']
    long_texts = ['long_text1', 'long_text2']
    
    def __init__(self, *args, **kwargs):
        cls = self.__class__
        setattr(cls, 'text1', CF('text1', **CNNE))
        cls.text1 = CF('text1', **CNNE)
        super().__init__(*args, **kwargs)

    # for e in texts:
    #     setattr(self, e, text(e))
    # for e in self.long_texts:
    #     long_text(e)
