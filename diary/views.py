import logging
import openai
import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render

from .forms import InquiryForm, DiaryCreateForm, DiaryAiForm
from .models import Diary
from django.conf import settings


logger = logging.getLogger(__name__)


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # URLに埋め込まれた主キーから日記データを1件取得。取得できなかった場合は404エラー
        diary = get_object_or_404(Diary, pk=self.kwargs['pk'])
        # ログインユーザーと日記の作成ユーザーを比較し、異なればraise_exceptionの設定に従う
        return self.request.user == diary.user


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 2


    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')


    def get_initial(self):
        initial = super().get_initial()
        content = self.request.session.get('content')
        title = self.request.session.get('title')
        if content is not None:
            initial['content'] = content
            initial['title'] = title
        self.request.session.pop('content', None)
        self.request.session.pop('title', None)
        return initial

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)

class DiaryAiCreateView(LoginRequiredMixin, generic.FormView):
    model = Diary
    template_name = 'diary_ai.html'
    form_class = DiaryAiForm
    success_url = reverse_lazy('diary:diary_create')

    def form_valid(self, form):

        api_key = form.cleaned_data['api_key']
        event_1 = form.cleaned_data['event']
        # event_2 = form.cleaned_data['event2']
        # event_3 = form.cleaned_data['event3']
        # event_4 = form.cleaned_data['event4']
        # event_5 = form.cleaned_data['event5']


        if api_key == os.environ.get('SECRET_WORD'):
            openai.api_key = os.environ.get('API_KEY')
        # else:
        #     openai.api_key = api_key

        #ChatGPT
        response_content = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "箇条書きで与えられた文章から日記を作成してください"
                },
                {
                    "role": "user",
                    "content": event_1
                },
                # {
                #     "role": "user",
                #     "content": event_2
                # },
                # {
                #     "role": "user",
                #     "content": event_3
                # },
                # {
                #     "role": "user",
                #     "content": event_4
                # },
                # {
                #     "role": "user",
                #     "content": event_5
                # },
            ],
        )
        content = response_content["choices"][0]["message"]["content"]

        response_title = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "文章のタイトルを生成してください"
                },
                {
                    "role": "user",
                    "content": content
                },
            ],
        )
        title = response_title["choices"][0]["message"]["content"]

        self.request.session['content'] = content
        self.request.session['title'] = title

        # form = DiaryCreateForm(initial = {
        #     'title': title,
        #     'content': content,
        # })
        # form.initial['title'] = title
        # form.initial['content'] = content

        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "生成に失敗しました")
        return super().form_invalid(form)






