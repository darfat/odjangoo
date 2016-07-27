from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
import xmlrpclib
from django.shortcuts import redirect


#user = 'IAMONLYHUMAN'
#pwd = 'noalarmandnosurprises'
user = 'admin'
pwd = 'admin'
dbname = 'skp_v4_prov_jabar'
#dbname ='skp_v4_prov_jabar_live'
model = 'res.partner'
#server_common='http://skp.jabarprov.go.id:5069/xmlrpc/common' #9469
#server_object='http://skp.jabarprov.go.id:5069/xmlrpc/object' #8071
server_common='http://localhost:9469/xmlrpc/common'
server_object='http://localhost:9469/xmlrpc/object'


def index(request):
    t = loader.get_template('skpcomplaint/index.html')
    c = Context({
        'employee_list': [],
        'status':'new'
    })
    return HttpResponse(t.render(c))

def search(request):

    t = loader.get_template('skpcomplaint/search.html')
    sock = xmlrpclib.ServerProxy(server_common)
    uid = sock.login(dbname ,user ,pwd)
    sock = xmlrpclib.ServerProxy(server_object)
    key=request.POST.get('key_word',"")

    # SEARCH PARTNERS
    if key[:1]=='1':
        args = [('nip', 'like', key)]
    else:
        args = [('lower_fullname', 'like', key.lower())]
    ids = sock.execute(dbname, uid, pwd, model, 'search', args)
    # READ PARTNER DATA
    fields = ['name', 'nip','job_id','company_id','parent_id','image_medium']
    results = sock.execute(dbname, uid, pwd, model, 'read', ids, fields)

    c = Context({
        'employee_list': results,

    })
    #return render(request,c)
    #return render_to_response('search.html',
    #                          c,
    #                          context_instance=RequestContext(request))
    return HttpResponse(t.render(c))
def detail(request, employee_id):
    t = loader.get_template('skpcomplaint/detail.html')
    sock = xmlrpclib.ServerProxy(server_common)
    uid = sock.login(dbname ,user ,pwd)
    sock = xmlrpclib.ServerProxy(server_object)

    # SEARCH PARTNERS
    args = [('id', '=', employee_id),]
    ids = sock.execute(dbname, uid, pwd, model, 'search', args)
    # READ PARTNER DATA
    fields = ['name', 'nip','job_id','company_id','parent_id','image_medium']
    results = sock.execute(dbname, uid, pwd, model, 'read', ids, fields)
    c = Context({
        'employee_list': results,
         })
    return HttpResponse(t.render(c))
def results(request, employee_id):
    return HttpResponse("Submit Berhasil %s." % employee_id)
def propose(request, employee_id):
    t = loader.get_template('skpcomplaint/index.html')
    sock = xmlrpclib.ServerProxy(server_common)
    uid = sock.login(dbname ,user ,pwd)
    sock = xmlrpclib.ServerProxy(server_object)
    complaint_employee_model='project.perilaku.complaint'

    complaint_id_source=request.POST.get('input_source_id',"")
    complaint_name_source = request.POST.get('input_source_name',"")
    complaint_phone_source = request.POST.get('input_phone',"")
    complaint_source = request.POST.get('input_complaint_type',"")
    notes = request.POST.get('input_notes',"")

    #CREATE complaint_employee_model
    complaint_data = {'employee_id':employee_id, 'complaint_id_source':complaint_id_source, 'complaint_name_source':complaint_name_source,
                      'complaint_phone_source':complaint_phone_source, 'complaint_source':complaint_source,'notes':notes,
                      'state':'new'}
    complaint_id = sock.execute(dbname, uid, pwd, complaint_employee_model, 'create', complaint_data)
    status_input='failed';
    if complaint_id :
        status_input='done';
    c = Context({
        'employee_list': [],
        'status':status_input
    })
    #return HttpResponse(t.render(c))
    return redirect('../../')
