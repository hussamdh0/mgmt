from core.abstract import *


class TaskManager(MGR):
    def main_tasks(self, qs=None):
        if not qs:
            qs = super(TaskManager, self).get_queryset()
        return qs.filter(parent=None)

    def sub_tasks(self, qs=None):
        if not qs:
            qs = super(TaskManager, self).get_queryset()
        ids = self.main_tasks().values_list('id', flat=True)
        return qs.filter(parent__id__in=ids)
    
    def sub_sub_tasks(self, qs=None):
        if not qs:
            qs = super(TaskManager, self).get_queryset()
        ids = self.sub_tasks().values_list('id', flat=True)
        return qs.filter(parent__id__in=ids)

    def remaining_tasks(self, qs=None):
        if not qs:
            qs = super(TaskManager, self).get_queryset()
        ids1 =  self.main_tasks().values_list('id', flat=True)
        ids2 = self.sub_tasks().values_list('id', flat=True)
        ids3 = self.sub_sub_tasks().values_list('id', flat=True)
        return qs.exclude(
            Q(id__in=ids1) | Q(id__in=ids2) | Q(id__in=ids3)
        )
    
    def self_and_children_tasks(self, pk, qs=None):
        if not qs:
            qs = super(TaskManager, self).get_queryset()
        return qs.filter(root_pk=pk)
        

class Task(BaseModel):
    objects         = TaskManager()
    parent          = FK('self', **FKKW)
    important       = BF(default=False)
    done            = BF(default=False)
    all_done        = BF(default=False)
    root_pk         = IF(**NNN)
    description     = TF(**NNE)
    
    
    @property
    def _all_done(self):
        for item in self.task_set.all():
            if item.done == False:
                return False
        return self.done
    
    @property
    def _root_pk(self):
        root = self
        while(True):
            if not root.parent:
                break
            root = root.parent
        return root.pk

    @property
    def non_completed_tasks(self):
        result = ''
        for item in self.task_set.all():
            result += f'{item.non_completed_tasks}\n'
        if self.done == False:
            result = f'{self.name}\n' + result
        if result != '' and result[-1] == '\n':
            result = result[:-1]
        return result

    @property
    def desc(self):
        if hasattr(self, 'pk') and getattr(self, 'pk'):
            if self.all_done != self._all_done or self.root_pk != self._root_pk:
                self.save()
        
        if len(self.description) > 25:
            return self.description[:25] + '...'
        return self.description
    
    def save(self, *args, **kwargs):
        self.all_done = self._all_done
        self.root_pk  = self._root_pk
        super(Task, self).save(*args, **kwargs)
        
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)




# class TaskItem(BaseModel):
#     task            = FK(Task, **FKKW)
#     done            = BF(default=False)

# admin.site.register(Task)
# admin.site.register(TaskItem)
