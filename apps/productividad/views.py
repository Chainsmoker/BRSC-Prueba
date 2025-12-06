from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from apps.control_expediente.models import RegistroActividad

from .models import DailyActivity
from .forms import ActivityForm, ScoreForm

User = get_user_model()

class ActivityFormAjaxView(LoginRequiredMixin, View):
    def get(self, request):
        date = request.GET.get("date")
        form = ActivityForm(initial={'date': date})

        if getattr(request.user, 'role', 0) == 3:
            activities = DailyActivity.objects.filter(
                date=date
            ).order_by("user__first_name", "title")
        else:
            activities = DailyActivity.objects.filter(
                user=request.user,
                date=date
            ).order_by("title")

        html = render_to_string(
            "productivity/activity_form_modal.html",
            {
                "form": form,
                "activities": activities,
                "date": date,
            },
            request=request
        )

        return JsonResponse({"html": html})

class CalendarView(LoginRequiredMixin, View):
    def get(self, request):
        users = None
        if request.user.is_staff or getattr(request.user, 'is_superuser', False) or getattr(request.user, 'is_admin', False):
            users = get_user_model().objects.order_by('first_name')

        registro_actividad = RegistroActividad.objects.all().order_by('-fecha')

        usuarios = (
            get_user_model().objects.filter(is_active=True)
            .exclude(username__in=['plupa', 'cdiaz'])
            .order_by('first_name')
        )

        return render(request, 'productivity/calendar.html', {
            'users': users,
            'registro_actividad': registro_actividad,
            'usuarios': usuarios,
        })

class EventsApiView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_id = request.GET.get('user_id')

        if user_id and (request.user.is_staff or getattr(request.user, 'is_admin', False) or request.user.is_superuser):
            user = get_user_model().objects.filter(id=user_id).first() or user

        qs = DailyActivity.objects.filter(user=user)

        events = []
        for a in qs:
            if a.score == 1:
                color = 'red'
            elif a.score == 2:
                color = 'orange'
            elif a.score == 3:
                color = 'green'
            else:
                color = "#3A7175"

            events.append({
                'id': a.id,
                'title': a.title,
                'start': a.date.isoformat(),
                'allDay': True,
                'color': color,
            })

        return JsonResponse(events, safe=False)

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = DailyActivity
    form_class = ActivityForm
    template_name = 'productivity/activity_form.html'

    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get('date')
        if date:
            initial['date'] = date
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save()

        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('productivity:calendar')

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyActivity
    form_class = ActivityForm
    template_name = 'productivity/activity_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user and not request.user.is_staff and not getattr(request.user, 'is_admin', False):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('productivity:calendar')

class ScoreActivityView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or getattr(request.user, 'is_admin', False) or request.user.is_superuser):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        activity = get_object_or_404(DailyActivity, pk=pk)
        form = ScoreForm(initial={'score': activity.score})
        return render(request, 'productivity/score_form.html', {'form': form, 'activity': activity})

    def post(self, request, pk):
        activity = get_object_or_404(DailyActivity, pk=pk)
        form = ScoreForm(request.POST)
        if form.is_valid():
            activity.score_activity(request.user, int(form.cleaned_data['score']))
            return JsonResponse({'ok': True, 'score': activity.score})
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

class UserReportView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if not (request.user.is_staff or getattr(request.user, 'is_admin', False) or request.user.is_superuser):
            return HttpResponseForbidden()

        user_model = get_user_model()
        target = get_object_or_404(user_model, id=user_id)

        qs = DailyActivity.objects.filter(user=target)
        summary = qs.values('date__year', 'date__month').annotate(
            avg_score=Avg('score'),
            activities=Count('id')
        ).order_by('-date__year', '-date__month')

        paginator = Paginator(qs.order_by('-date'), 50)
        page = request.GET.get('page', 1)
        activities_page = paginator.get_page(page)

        return render(request, 'productivity/user_report.html', {
            'target': target,
            'summary': summary,
            'activities': activities_page,
        })

class ActivityEditAjaxView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.activity = get_object_or_404(DailyActivity, pk=kwargs['pk'])
        if self.activity.user != request.user and not request.user.is_staff and not getattr(request.user, 'is_admin', False):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        form = ActivityForm(instance=self.activity)
        html = render_to_string("productivity/activity_edit_modal.html", {
            "form": form,
            "activity": self.activity,
        }, request=request)
        return JsonResponse({"html": html})

    def post(self, request, pk):
        form = ActivityForm(request.POST, instance=self.activity)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
