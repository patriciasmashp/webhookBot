from infra.IFaces.IHandler import IHandler

class Handler(IHandler):
    """Класс обработчик события"""

    _handler_filter = None
    
    def __init__(self, callback, handler_filter):
        self.callback = callback
        self._handler_filter = handler_filter

    def __call__(self, *args, **kwds):
        
        return self.callback(*args)
