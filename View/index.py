# coding=utf-8
import HttpIO;
import router;
from Lib import Template;
@router.Router("/",True)
def index(HttpRequest,Session):
    #return HttpIO.HttpResponse(str(HttpRequest.POST['name']).replace("\r\n","<br/>"));
    return HttpIO.HttpResponse(str((HttpRequest.POST,HttpRequest.FILE)))
    return Template.View("index.html",{});
