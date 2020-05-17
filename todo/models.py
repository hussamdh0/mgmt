from core.abstract import *


class Task(BaseModel):
    parent          = FK('self', **FKKW)
    important       = BF(default=False)
    done            = BF(default=False)
    all_done        = BF(default=False)
    description     = TF(**NNE)
    
    
    @property
    def _all_done(self):
        for item in self.task_set.all():
            if item.done == False:
                return False
        return self.done

    @property
    def desc(self):
        if len(self.description) > 25:
            return self.description[:25] + '...'
        return self.description
    
    def save(self, *args, **kwargs):
        self.all_done = self._all_done
        super(Task, self).save(*args, **kwargs)
        
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        if hasattr(self, 'pk') and getattr(self, 'pk'):
            if self.all_done != self._all_done:
                self.save()



# class TaskItem(BaseModel):
#     task            = FK(Task, **FKKW)
#     done            = BF(default=False)

# admin.site.register(Task)
# admin.site.register(TaskItem)
