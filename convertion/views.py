from django.http import *
from django.template import RequestContext, loader
from .forms import ConvertForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    template = loader.get_template('convertion/index.html')
    if request.method == 'POST':
        form = ConvertForm(request.POST)
        if request.is_ajax:
            num = request.POST["number"]# get ajax value
            rom= convert(int(num)) # convert 
            response_data = {'number':num,'convert':rom}
            return HttpResponse( json.dumps(response_data),content_type="application/json")
    else:
        form = ConvertForm()
    context = RequestContext(request, {'form':form })
    return HttpResponse(template.render(context))

def convert(number):
    rom = {'1':'I','5':'V','10':'X','50':'L','100':'C','500':'D','1000':'M'}
    preview = {'0':'V','1':'L','2':'D'}
    preview9 = {'0':'X','1':'C','2':'M'}
    preview2 = {'0':'I','1':'X','2':'C'}
    new = decompose(number)
    print new
    romain = ''
    for n in new.split('+'):
        if n in rom: 
            romain +=rom[n]
        else:
            size = len(n)-1
            puiss = 10**size
            num = int(n)//puiss
            if 1<num<=3 and str(puiss) in rom:
                romain += ''.join([ rom[str(puiss)] for i in range(num)])
            elif 5<num<=8:
                romain +=preview[str(size)]
                romain += ''.join([ preview2[str(size)] for i in range(num-5)])
            elif num == 4:
                romain += preview2[str(size)]
                romain +=preview[str(size)]
            elif num == 9:
                romain += preview2[str(size)]
                romain +=preview9[str(size)]
    return romain
def decompose(number):
    size = len(str(number))-1
    new = ''
    while size>=0:
        sign = ''
        puiss = 10**size
        num = number//puiss
        number -=num*puiss
        if number !=0: sign = '+'
        if num !=0: new +=str(num*puiss)+sign
        size -=1
        if number==0:
            break
    return new
    
    