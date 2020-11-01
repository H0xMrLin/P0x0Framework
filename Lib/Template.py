#encoding:utf-8
import re;
import traceback
import HttpIO;
TemplatePath="View/_Template/"
def View(TempFileName,Paramters={},PrintBaseInfo=False):
    Data=Paramters;
    TemplateContent= (open(TemplatePath+TempFileName,"rb").read()).decode("utf-8");
    if(PrintBaseInfo):
        TemplateContent="<!-- Template:{{TempFileName}} DataCount:{{len(Data)}} -->"+TemplateContent
    TemplateAim= re.findall("{{(.+?)}}",TemplateContent);
    for EvalCode in TemplateAim:
        try:
            TemplateContent=TemplateContent.replace("{{"+EvalCode+"}}",str(eval(EvalCode)));
        except:
            print(traceback.format_exc());
            None;
    return HttpIO.HttpResponse(TemplateContent);

    