from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Property, Inquiry
from django.db.models import Sum
from django.db.models import Q

def home_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.profile.role == "owner":
                return redirect("owner_dashboard")
            else:
                return redirect("tenant_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "home.html")
def register_view(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            print("Passwords do not match")

        elif User.objects.filter(username=username).exists():
            print("Username already exists")

        elif User.objects.filter(email=email).exists():
            print("Email already registered")

        else:
            print("Everything is correct")

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            Profile.objects.create(
             user=user,
             role=role
            )
            user.save()
            if role == "owner":
              return redirect("owner_dashboard")
            else:
              return redirect("tenant_dashboard")
    return render(request, "register.html")
  
def owner_dashboard(request):

    properties = Property.objects.filter(owner=request.user)
    total_views = properties.aggregate(
    Sum("views")
    )["views__sum"] or 0

    total_properties = properties.count()

    inquiries = Inquiry.objects.filter(
        property__owner=request.user
    )

    interested_tenants_count = inquiries.count()

    return render(
        request,
        "owner_dashboard.html",
        {
            "properties": properties,
            "total_properties": total_properties,
            "interested_tenants_count": interested_tenants_count,
            "total_views": total_views,
        }
    )


def tenant_dashboard(request):

    search = request.GET.get("search")

    properties = Property.objects.filter(
        status="Available"
    )

    if search:

        properties = properties.filter(
            Q(city__icontains=search) |
            Q(title__icontains=search)
        )

    return render(
        request,
        "tenant_dashboard.html",
        {
            "properties": properties
        }
    )
def add_property(request):

    if request.method == "POST":

        title = request.POST.get("title")
        city = request.POST.get("city")
        address = request.POST.get("address")
        rent = request.POST.get("rent")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        status = request.POST.get("status")
        Property.objects.create(
            owner=request.user,
            title=title,
            city=city,
            address=address,
            rent=rent,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            description=description,
            image=image,
            status = status,
        )

        return redirect("owner_dashboard")   # <-- Add this

    return render(request, "add_property.html")

def edit_property(request, property_id):

    property = Property.objects.get(id=property_id)

    if request.method == "POST":

        property.title = request.POST.get("title")
        property.city = request.POST.get("city")
        property.address = request.POST.get("address")
        property.rent = request.POST.get("rent")
        property.bedrooms = request.POST.get("bedrooms")
        property.bathrooms = request.POST.get("bathrooms")
        property.description = request.POST.get("description")
        property.status = request.POST.get("status")
        property.save()

        return redirect("owner_dashboard")

    return render(
        request,
        "edit_property.html",
        {
            "property": property
        }
    )


def delete_property(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id,
        owner=request.user
    )

    property.delete()

    return redirect("owner_dashboard")
def logout_view(request):
    logout(request)
    return redirect("home")
from django.shortcuts import get_object_or_404

def property_details(request, property_id):

    property = Property.objects.get(id=property_id)

    property.views += 1
    property.save()

    return render(
        request,
        "property_details.html",
        {
            "property": property
        }
    )

def contact_owner(request, property_id):

    property = Property.objects.get(id=property_id)

    if request.method == "POST":

        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Inquiry.objects.create(
            tenant=request.user,
            property=property,
            phone=phone,
            message=message
        )

        return redirect("tenant_dashboard")

    return render(
        request,
        "contact_owner.html",
        {
            "property": property
        }
    )

def interested_tenants(request):

    inquiries = Inquiry.objects.filter(
        property__owner=request.user
    )

    return render(
        request,
        "interested_tenants.html",
        {
            "inquiries": inquiries
        }
    )