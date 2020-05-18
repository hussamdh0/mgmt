from core.abstract import *
from django.db.models import Sum, Value, Aggregate
from django.db.models.functions import Coalesce


class TaskManager(MGR):
    def get_queryset(self):
        qs = super(TaskManager, self).get_queryset()
        return qs.annotate(due=Sum('task__pk'))
    
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
        ids1 = self.main_tasks().values_list('id', flat=True)
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
    subtasks_done   = BF(**NNN)
    root_pk         = IF(**NNN)
    description     = TF(**NNE)
    
    @property
    def _all_done(self):
        for item in self.task_set.all():
            if item._all_done == False:
                return False
        return self.done
    
    @property
    def _subtasks_done(self):
        pks = self.subtasks_pks()
        if len(pks) == 0:
            return None
        q = Task.objects.filter(pk__in=pks).values_list('done', flat=True)
        if False in q:
            return False
        return True
        # for item in self.task_set.all():
        #     result = True
        #     if item._all_done == False:
        #         return False
        # return result
    
    def subtasks_pks(self):
        l = list(self.task_set.all().values_list('pk', 'task__pk', 'task__task__pk', 'task__task__task__pk'))
        x = {e for t in l for e in t if e}
        return x
    
    @property
    def _root_pk(self):
        root = self
        while (True):
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
        if len(self.description) > 25:
            return self.description[:25] + '...'
        return self.description
    
    @property
    def full_name(self):
        # if hasattr(self, 'pk') and getattr(self, 'pk'):
        #     if self.subtasks_done != self._subtasks_done:
        #             #or self.root_pk != self._root_pk
        #         self.save()
        
        if not self.parent:
            return self.name
        return f'{self.parent.full_name} : {self.name}'
    
    def refresh(self):
        if hasattr(self, 'pk') and getattr(self, 'pk'):
            _subtasks_done = self._subtasks_done
            _root_pk = self._root_pk
            kwargs = {'refresh': True}
            if self.subtasks_done != _subtasks_done:
                kwargs['subtasks_done'] = _subtasks_done
            if self.root_pk != _root_pk:
                kwargs['root_pk'] = _root_pk
            if len(kwargs.keys()) > 1:
                self.save(**kwargs)
    
    def save(self, *args, **kwargs):
        refresh = kwargs.pop('refresh', False)
        if refresh:
            _subtasks_done          = kwargs.pop('subtasks_done', None)
            _root_pk                = kwargs.pop('root_pk', None)
        else:
            _subtasks_done          = kwargs.pop('subtasks_done', self._subtasks_done)
            _root_pk                = kwargs.pop('root_pk', self._root_pk)
        if _subtasks_done:
            self.subtasks_done      = _subtasks_done
        if _root_pk:
            self.root_pk            = _root_pk
        super(Task, self).save(*args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

# class TaskItem(BaseModel):
#     task            = FK(Task, **FKKW)
#     done            = BF(default=False)

# admin.site.register(Task)
# admin.site.register(TaskItem)
