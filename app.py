import grok
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from willdo.interfaces import IDoItTomorrow, IWillDoList
import datetime


class ManageList(grok.Permission):
    grok.name('willdo.ManageList')
    grok.title('Manage willdo list')


class DoItTomorrow(grok.Application, grok.Container):
    implements(IDoItTomorrow)


class WillDo(grok.Model):
    implements(IWillDoList)

    def __init__(self, day=None):
        super(WillDo, self).__init__()
        if day is None:
            self.day = datetime.date.today()
        else:
            self.day = day
        self.tasks = PersistentList()
        self.closed = False


class DoItTomorrowIndex(grok.View):
    grok.context(DoItTomorrow)
    grok.name('index')
    grok.require('willdo.ManageList')

    def update(self, day=u'', month=u'', year=u'',
               today=None, tomorrow=None):
        # We require that one of these is supplied:
        if today is None and tomorrow is None and day == u'':
            return
        thisday = datetime.date.today()
        if today is not None:
            target = thisday
        if tomorrow is not None:
            target = datetime.date.fromordinal(thisday.toordinal() + 1)
        else:
            if day == u'':
                day = thisday.day
            else:
                day = int(day)
            if month == u'':
                month = thisday.month
            else:
                month = int(month)
            if year  == u'':
                year = thisday.year
            else:
                year = int(year)
            target = datetime.date(year, month, day)

        id = unicode(target.toordinal())
        if self.context.has_key(id):
            return
        self.context[id] = WillDo(day=target)

    def entries(self):
        context = self.context
        contents = []
        for key in context.keys():
            info = dict(
                link = self.url(key),
                day = context[key].day,
                )
            contents.append(info)
        return contents

    def todayslist(self):
        context = self.context
        thisday = datetime.date.today()
        key = unicode(thisday.toordinal())
        if key not in context.keys():
            return None
        tl = context[key]
        info = dict(
            link = self.url(key),
            day = tl.day,
            tasks = tl.tasks,
            closed = tl.closed,
            )
        return info


class WillDoIndex(grok.View):
    grok.context(WillDo)
    grok.name('index')
    grok.require('willdo.ManageList')

    def update(self, open=None, close=None, newtask=None):
        if open:
            self.context.closed = False
        if close:
            self.context.closed = True
        if newtask:
            if self.context.closed:
                # should not happen, as the add form should not be
                # visible then
                pass
            else:
                new = dict(
                    name = newtask,
                    #time = datetime.timedelta(0),
                    time = 0, # minutes
                    start = None,
                    )
                newdict = PersistentDict(new)
                self.context.tasks.append(newdict)
        now = datetime.datetime.utcnow()
        for key in self.request.form.keys():
            if key.startswith(u'start-'):
                started = [task for task in self.context.tasks if task['start'] is not None]
                for task in started:
                    diff = now - task['start']
                    task['time'] += int(round((now - task['start']).seconds / 60.0))
                    task['start'] = None
                try:
                    id = int(key[6:])
                except:
                    return
                task = self.context.tasks[id]
                task['start'] = now


class Edit(grok.EditForm):
    grok.context(WillDo)
    grok.require('willdo.ManageList')
