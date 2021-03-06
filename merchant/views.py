from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, ProcessFormView
from django.contrib.auth.models import User 
from django.contrib import auth
from django import forms
from .forms import *
from .models import *
from django.http import *
from django.shortcuts import render_to_response
from  django.template import RequestContext
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
            rcontext = RequestContext(request, locals())
            return render_to_response(MerchantHomeView.template_name, rcontext)
        else:
            rcontext = RequestContext(request, locals())
            return render_to_response(MerchantHomeView.template_name, rcontext)
    else:
        return HttpResponseRedirect("/merchant/")


def logout_view(request):
    user = request.user
    if user is not None:
        auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/merchant/")


class RegisterView(FormView):
    template_name = 'merchant/register.html'
    form_class = RegisterForm
    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        ###process register form
        if self.request.method == 'POST':
            form_reg = RegisterForm(self.request.POST)
            if form_reg.is_valid():
                username = form_reg.cleaned_data['email']
                user = User.objects.create_user(username = username,
                                            password = form_reg.cleaned_data['password'],
                                            email = form_reg.cleaned_data['email'])
                merchant = Merchant(user = user)
                merchant.city = form_reg.cleaned_data['city']
                merchant.address = form_reg.cleaned_data['address']
                print("longitude is :" + form_reg.cleaned_data['longitude'])
                merchant.longitude = float(form_reg.cleaned_data['longitude'])
                merchant.latitude = form_reg.cleaned_data['latitude']
                merchant.description = form_reg.cleaned_data['description']
                user.save()
                merchant.save()
            else:
                print("error: not post?")
        return super(RegisterView, self).form_valid(form)


class MerchantMainPageView(TemplateView):
    template_name = 'merchant/mainpage.html'
    def get_context_data(self, **kwargs):
        context = super(MerchantMainPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context


class MerchantHomeView(TemplateView):
    template_name = 'merchant/merchant_home.html'
    def get_context_data(self, **kwargs):
        context = super(MerchantHomeView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context


class CommercialListView(TemplateView):
    template_name = 'merchant/commercial_list.html'
    def get_context_data(self, **kwargs):
        context = super(CommercialListView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        user = self.request.user
        clist = []
        clist = Commercial.objects.filter(merchant__username = user.username)
        context['commercial_list'] = clist
        return context
    
    
    
class CommercialPostView(FormView):
    form_class = PostCommercialForm
    template_name = 'merchant/commercial_post.html'
    def get_context_data(self, **kwargs):
        context = super(CommercialPostView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['post_form'] = PostCommercialForm()
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        ###process register form
        if self.request.method == 'POST':
            form_post = PostCommercialForm(self.request.POST, self.request.FILES)
            if form_post.is_valid():
                temp = form_post.save(commit=False)
                temp.merchant = self.request.user
                if self.request.FILES:
                    temp.photo = self.request.FILES['photo']
		    if 'photo1' in list(self.request.FILES):
		        temp.photo1 = self.request.FILES['photo1']
		    if 'photo2' in list(self.request.FILES):
                        temp.photo2 = self.request.FILES['photo2']
                temp.save()
            else:
                print(form_post.errors)
                print("form_post not valid")
        return super(CommercialPostView, self).form_valid(form)

