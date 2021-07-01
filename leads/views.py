from django.db.models import query
from djcrm import settings
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    CreateView,
    FormView
)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from .models import Lead, Agent, Category
from .forms import LeadModelForm, LeadCategoryUpdateForm, CustomUserCreatingForm, AssignAgentForm
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OraniserandLoginRequiredMixin

class LandingPage(TemplateView):
    template_name = 'djcrm/landing.html'


class LeadList(LoginRequiredMixin, ListView):
    template_name = "leads/leads.html"
    context_object_name = 'leads'

    def get_queryset(self):
        queryset = Lead.objects.all()
        # checking if the current logged in user is an organiser
        if self.request.user.is_organizer:
            queryset = queryset.filter(
                organization=self.request.user.userprofile, agent__isnull=False)
        else:
            queryset = queryset.filter(
                agent__user=self.request.user, agent__isnull=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadList, self).get_context_data(**kwargs)
        if self.request.user.is_organizer:
            queryset = Lead.objects.filter(
                organization=self.request.user.userprofile, agent__isnull=True)

            context.update({
                'unassigned_leads': queryset
            })
        return context

class LeadDetail(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


    context_object_name = 'lead'

class LeadUpdate(OraniserandLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm
    context_object_name = 'lead'

    def get_queryset(self):
        queryset = Lead.objects.all()
        # checking if the current logged in user is an organiser
        queryset = queryset.filter(
            organization=self.request.user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse('leads:leads')

class LeadDelete(OraniserandLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        queryset = Lead.objects.all()
        # checking if the current logged in user is an organiser
        queryset = queryset.filter(
            organization=self.request.user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse('leads:leads')

class LeadCreate(OraniserandLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:leads')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        # send_mail(
        #     subject=f'New Lead is created',
        #     recipient_list=[],
        #     message=f"Go the site and the new lead"
        # )
        return super(LeadCreate, self).form_valid(form)

class SignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreatingForm

    def get_success_url(self):
        return reverse('leads:leads')

class AssignAgentView(OraniserandLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:leads")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryList(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
            context.update({
                "unassigned_lead_count": Lead.objects.filter(organization=user.userprofile, category__isnull=True).count()
            })
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset

class CategoryDetail(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset

class LeadCategoryUpdate(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self) -> str:
        return reverse('leads:leads')

class CategoryUpdate(OraniserandLoginRequiredMixin, ListView):
    template_name = "leads/category_update.html"

class CategoryDelete(OraniserandLoginRequiredMixin, ListView):
    template_name = "leads/category_delete.html"

class CategoryCreate(OraniserandLoginRequiredMixin, ListView):
    template_name = "leads/category_create.html"