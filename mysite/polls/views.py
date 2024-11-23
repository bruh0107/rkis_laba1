from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.management.commands.changepassword import UserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView

from .forms import RegistrationForm, ProfileUpdateForm
from .models import Question, Choice, User
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic, View


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class Registration(generic.CreateView):
    template_name = 'polls/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('polls:login')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из аккаунта.')
    return redirect('polls:login')

class Profile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'polls/profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user = self.request.user
        if not user.avatar:
            messages.error(self.request, 'Пожалуйста, загрузите аватар.')
            return user

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'polls/profile_update.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('polls:profile')
        return render(request, 'polls/profile_update.html', {'form': form})

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'polls/profile_confirm_delete.html'
    success_url = reverse_lazy('polls:index')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Ваш профиль был успешно удален')
        return super().delete(request, *args, **kwargs)
