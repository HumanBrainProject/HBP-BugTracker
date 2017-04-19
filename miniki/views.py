
'''Views'''

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect 

from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
import hbp_app_python_auth.settings as auth_settings
import requests

from django.views.generic.list import ListView
from django.views.generic.base import  TemplateView, View
from django.views.generic.detail import DetailView


from django.shortcuts import render_to_response 
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404

from django.core.urlresolvers import reverse
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import bleach

from markdown import markdown
from .forms import TicketForm
from .forms import HomeForm
from .forms import CommentForm
from .forms import ProjectForm

from .models import Ticket
from .models import Home
from .models import Project
from .models import Comment

from .utils.ctx_handler import post_temp_user_ctx, get_temp_user_ctx
import json
from django.core import serializers


# def form_valid(self, form):

#     self.object = form.save()
#     print('blav')
#     # Envoi d'un message a l'utilisateur

#     messages.success(self.request, "Votre profil a ete mis a jour avec succes.")

#     return HttpResponseRedirect(self.get_success_url())

class ProjectListView(ListView): 
    model = Project
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        return context

    def projects(self):
        return Project.objects.filter()

@login_required(login_url='/login/hbp')
def create_project(request):
    '''Render the wiki create form'''

    try:
        p = Project.objects.get()
        content = markdown(p.text) 
    except Project.DoesNotExist:                
        p = Project()
        
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=p)

        if form.is_valid():
            p = form.save(commit=False)
            p.save()

    form = ProjectForm(instance=p)

    return render(request, 'create_project.html', {'form': form, 'ctx': self.kwargs['ctx']})



@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class HomeView(TemplateView):
    # context = UUID(request.GET.get('ctx'))
    template_name = "home.html"
    model = Home
    form_class = HomeForm
    

    def projects(self):
        return Home.objects.get()

    def get(self, request, *args, **kwargs):
        if not _is_collaborator(request):
            return HttpResponseForbidden()
        try:)
            h = Home.objects.get()
        except Home.DoesNotExist:
            h = Home()
        form = self.form_class(instance = h)

        return render(request, self.template_name, {'form': form, 'ctx': request.META['QUERY_STRING']})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
                 # Clean up user input
            form.save()
        return render(request, self.template_name, {'form': form, 'ctx': self.kwargs['ctx']})




@login_required(login_url='/login/hbp')
def Test_Menu_deroulant(request):
    '''Render the wiki page using the provided context query parameter''' 
    try:
        ticket = Ticket.objects.get(ctx=context)
        content = markdown(ticket.text)  
    except Ticket.DoesNotExist:                  
        ticket = None
        content = ''
    return render(request,'Test_Menu_deroulant.html', {'ticket': ticket, 'content': content})







# @login_required(login_url='/login/hbp')
# def edit_ticket(request):
#     '''Render the wiki edit form using the provided cofrom django.conf import settings
# from django.http import HttpResponseForbidden

# from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
# import hbp_app_python_auth.settings as auth_settings
# ntext query parameter'''

#     if not _is_collaborator(request):
#         return HttpResponseForbidden()

#     context = UUID(request.GET.get('ctx'))
#     # get or build the wiki page
#     try:
#         #ticket_page = TicketPage.objects.get(ctx=context)
#         ticket = Ticket.objects.get(ctx=context)
#     #except TicketPage.DoesNotExist:
#     except Ticket.DoesNotExist:                    
#         #ticket_page = TicketPage(ctx=context)
#         ticket = Ticket(ctx=context)

#     if request.method == 'POST':
#         #form = TicketPageForm(request.POST, instance=ticket_page)
#         #form = TicketForm(request.POST, instance=ticket_page)
#         form = TicketForm(request.POST, instance=ticket)

#         if form.is_valid():
#             #ticket_page = form.save(commit=False)
#             ticket = form.save(commit=False)
#             # Clean up user inputm
#             #ticket_page.text = bleach.clean(ticket_page.text)
#             ticket.text = bleach.clean(ticket.text)
#             #ticket_page.save()
#             ticket.save()
#     else:
#         #form = TicketPageForm(instance=ticket_page)
#         form = TicketForm(instance=ticket)

#     return render(request, 'edit.html', {'form': form, 'ctx': str(context)})<<<<<<< HEAD


# def _reverse_url(view_name, context_uuid):
#     """generate an URL for a view including the ctx query param"""
#     print ("Passing by view edit_ticket _reverse_url ?")
    
#     return '%s?ctx=%s' % (reverse(view_name)  , context_uuid)

# @login_required(login_url='/login/hbp')
# def create_ticket(request):
#     '''Render the wiki create form'''

#     try:
#         t = Ticket.objects.get()
#         content = markdown(t.text) 
#     except Ticket.DoesNotExist:                     
#         t = Ticket(ctx=context)
        
#     if request.method == 'POST':

#         form = TicketForm(request.POST, instance=t)
#         print (form)

#         if form.is_valid():
#             t = form.save(commit=False)
#             t.created_by = 1
#             t.save()
#     return render(request, 'create_ticket.html', {'form': form })

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class CreateTicketView(TemplateView):
    # context = UUID(request.GET.get('ctx'))

    template_name = "create_ticket.html"
    model = Ticket
    form_class = TicketForm

    # kwargs

    def get(self, request, *args, **kwargs):
        # try:
        #     print("try")
        #     h = self.model.objects.get()
        #     print (h)
        # except self.model.DoesNotExist:
        h = Ticket()
        form = self.form_class(instance = h)

        return render(request, self.template_name, {'form': form, 'ctx': self.kwargs['ctx']})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
                 # Clean up user input
            form.save()
            return self.redirect(request, self.kwargs['ctx'] )
        return render(request, self.template_name, {'form': form, 'ctx': self.kwargs['ctx']})

    @classmethod    
    def redirect(self, request, *args, **kwargs): ### use to go back to TicketListView directly after creating a ticket
        url = reverse('ticket-list2', kwargs = {'ctx': args})
        return HttpResponseRedirect(url)

def _is_collaborator(request):
    '''check access depending on context'''

    svc_url = settings.HBP_COLLAB_SERVICE_URL

    context = request.GET.get('ctx')
    if not context:
        return False
    url = '%scollab/context/%s/' % (svc_url, context)
    headers = {'Authorization': get_auth_header(request.user.social_auth.get())}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False
    collab_id = res.json()['collab']['id']
    url = '%scollab/%s/permissions/' % (svc_url, collab_id)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False
    return res.json().get('UPDATE', False)

def _get_access_token(request):
    return request.user.social_auth.get().extra_data['access_token']

@login_required(login_url='/login/hbp')
def config(request):
    '''Render the config file'''
    res = requests.get(settings.HBP_ENV_URL)
    config = res.json()

    # Use this app client ID
    config['auth']['clientId'] = auth_settings.SOCIAL_AUTH_HBP_KEY

    # Add user token informations
    config['auth']['token'] = {
        'access_token': _get_access_token(request),
        'token_type': get_token_type(request.user.social_auth.get()),
        'expires_in': request.session.get_expiry_age(),
    }
    
    # test = requests.get
    return JsonResponse(config)

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class TicketListView(ListView):  

    model = Ticket
    template_name = "ticket_list.html"


    def get(self, request, *args, **kwargs):
        #we do this here to make sure to catch the ctx
        post_temp_user_ctx (ctx=request.META['QUERY_STRING'], user_name=request.user)
        
        tickets = Ticket.objects.filter(id_project=0) ##need to change to get project id with collab
        ## add number of comments
        for ticket in tickets:
            ticket.nb_coms = self.get_nb_com(ticket.pk)                     
            
        return render(request, self.template_name, {'object': tickets, 'ctx': request.META['QUERY_STRING']}) #will nedd to replace all() by filter project
    @classmethod  
    def get_nb_com(self, pk):
        return Comment.objects.filter(ticket_id= pk).count()

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class TicketListView2(ListView):  
    model = Ticket
    template_name = "ticket_list.html"

    def get(self, request, *args, **kwargs):

        #we do this here to make sure to catch the ctx
        # post_temp_user_ctx (ctx=request.META['QUERY_STRING'], user_name=request.user)

        return render(request, self.template_name, {'object': Ticket.objects.all(), 'ctx': self.kwargs['ctx']}) #will nedd to replace all() by filter project

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class TicketDetailView(DetailView):

    model = Comment
    template_name = "ticket_detail.html"
    form_class = CommentForm

    def get_object(self):
        print ("Yes I go to get_object in detail !")
        
        return [Comment.objects.filter(ticket_id = self.kwargs['pk']), get_object_or_404(Ticket, pk=self.kwargs['pk']) ]
        

    def get_queryset (self):
        print ("Yes I go to get_queryset in detail !")
        
        return get_object_or_404(Ticket, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

    def get(self, request, *args, **kwargs):
        cmt = Comment()
        form = self.form_class(instance = cmt)

        return render(request, self.template_name, {'form': form, 'object': self.get_object(), 'ctx': self.kwargs['ctx'] })    

    @classmethod    
    def redirect(self, request, *args, **kwargs): ### use to go back to TicketListView directly after creating a ticket
        url = reverse('ticket-detail', kwargs = { 'pk':kwargs['pk'],'ctx': kwargs['ctx']})
        return HttpResponseRedirect(url)

    def post(self, request, *args, **kwargs):
        comment_creation = Comment()
        comment_creation.ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])      
       
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment_creation)

        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            return self.redirect(request, pk=self.kwargs['pk'], ctx=self.kwargs['ctx'])
        else :
            pass
            #faire passer un message...

        return render(request, 'ticket_list.html', {'form': p, 'ctx': self.kwargs['ctx']}) #need to change that       


    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL
        """
        model_instance = form.save(commit=False)
        model_instance.ticket = self.object
        # model_instance.author = self.request.user
        # model_instance.pub_date = datetime.now()
        # model_instance.publish = True

        model_instance.save()
        return HttpResponseRedirect(self.get_success_url())
