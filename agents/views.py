from django.shortcuts import render, redirect, reverse
from .mixins import OraniserandLoginRequiredMixin
from django.views import generic
from leads.models import Agent
from .forms import *
from random import randint
from django.core.mail import send_mail
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings





class AgentList(OraniserandLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        queryset = Agent.objects.filter(
            organization=self.request.user.userprofile
        )
        return queryset


class AgentCreate(OraniserandLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agents')

    def get_success_url(self):
        return reverse('agents:agents')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(str(randint(0, 2000000)))
        current_site = get_current_site(self.request)
        html_message = loader.render_to_string('mail/email.html',{
                'domain': current_site.domain,
                'user': user,
                'protocol': 'https'
        })
        send_mail(
            from_email=settings.FROM_EMAIL,
            subject='You are invited to be an agent',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
            message=None
        )
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        print('------------------------------------------------------------------------------')
        return super(AgentCreate, self).form_valid(form)


class AgentDetail(OraniserandLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = 'agent'

    def get_queryset(self):
        queryset = Agent.objects.filter(
            organization=self.request.user.userprofile
        )
        return queryset


class AgentDelete(OraniserandLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agents')

    def get_queryset(self):
        queryset = Agent.objects.filter(
            organization=self.request.user.userprofile
        )
        return queryset


class AgentUpdate(OraniserandLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    context_object_name = 'agent'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agents')

    def get_queryset(self):
        queryset = Agent.objects.filter(
            organization=self.request.user.userprofile
        )
        return queryset
