from django.shortcuts import render
from .models import About_Us

def about_us(request):
    """
    Renders the About Us page
    """
    about = About_Us.objects.all().order_by('-updated_on').first()

    return render(request, "about_us/about_us.html",
        {"about_us": about},
    )