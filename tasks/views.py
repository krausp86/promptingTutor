from django.shortcuts import render, redirect
from .models import Task, Progress

# Create your views here.
from django.contrib.auth.decorators import login_required
from tasks.services.llm_service import evaluate_prompt

@login_required
def task_view(request):
    user = request.user

    # Progress sicherstellen
    progress, created = Progress.objects.get_or_create(user=user)

    # aktuellen Task laden
    try:
        task = Task.objects.get(task_id=progress.current_level)
    except Task.DoesNotExist:
        return redirect("certificate")

    feedback = None

    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()

        if "submit" in request.POST:
            if not user_input:
                request.session['feedback'] = "Bitte gib zuerst einen Prompt ein."
                return redirect("task")

            ok, feedback = evaluate_prompt(user_input, task.task_text)

            if ok:
                progress.current_level += 1
                progress.save()
                return redirect("task")
            else:
                request.session['feedback'] = feedback
                return redirect("task")

    # Feedback aus der Session holen
    feedback = request.session.pop('feedback', None)

    return render(request, "tasks/task.html", {
        "task": task,
        "feedback": feedback
    })

@login_required
def certificate_view(request):
    return render(request, "tasks/certificate.html")
