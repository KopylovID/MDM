from ..forms import UAChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def ua_change_view(request):
    if request.method == "POST":
        form = UAChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("ma:index")
    else:
        form = UAChangeForm(instance=request.user)

    context = {"form": form}

    return render(
        request,
        "user_app/change.html",
        context,
    )
