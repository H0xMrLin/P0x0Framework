#Encoding:utf-8
import importlib;
import imp;
tmfp=open("ViewUrl.json")
ViewModels=eval(tmfp.read());
#url分配
urls={};
Models={};
for ModelName in ViewModels:
    Models[ModelName]=imp.reload( importlib.import_module(ModelName));
    #print(dir(Models));
    for Method in dir(Models[ModelName]):
        try:
            urls[(eval("Models['"+ModelName+"']."+Method+".RoutePath"))]=(eval("Models['"+ModelName+"']."+Method));
        except:
            None;