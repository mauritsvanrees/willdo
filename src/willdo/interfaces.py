from zope.interface import Interface
from zope.schema import List, TextLine, Bool, Date


class IDoItTomorrow(Interface):
    pass


class IWillDoList(Interface):

    day = Date(
        title = u"Day",
        description = u"Day that I will do the items on this list",
        required = True,
        )

    closed = Bool(
        title = u"Closed",
        description = u"Is this a closed list?",
        default = False,
        )

    tasks = List(
        title = u"Task list",
        description = u"List of tasks that I will do this day",
        required = False,
        value_type = TextLine(title=u"Task"),
        )
