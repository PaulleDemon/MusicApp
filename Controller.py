
class Notifier:

    _notify_lst = set()

    def register(self, cls):
        self._notify_lst.add(cls)

    def deRegister(self, cls):
        self._notify_lst.remove(cls)

    def notify(self, instance=None):

        if instance:
            for cls in self._notify_lst:
                if isinstance(cls, instance):
                    cls.notify()

        else:
            for cls in self._notify_lst:
                cls.notify()