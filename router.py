#encoding:utf-8
routes={};
def AddRouter(Path,func):
    routes[Path.strip()]=func;

def Controller(func):
    AddRouter(func.__name__,func);

"""
Useing eg:
    paramters(1) : Url partten to Path
    paramters(2) : Enable Path Cotroller 
    @Router('/index',True)
    def ...(HttpRequest):
        ...
        return HttpResponse....
"""

def Router(Path,Enable=True):
    def _AddAttr(func):
        if(Enable):
            setattr(func,'RoutePath',Path.strip());
            routes[Path.strip()]=func;
        return func;
    return _AddAttr;

