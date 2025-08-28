from django.shortcuts import render, redirect
from .forms import LocationForm
from django.contrib import messages
from core.models import Trip, Location, Status
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'core/home.html')


@login_required
def location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # if request.user.is_authenticated:
            student_faculty = form.cleaned_data['faculty']
            
            open_trip = Trip.objects.filter(status=Status.OPEN, locations__faculty=student_faculty).annotate(num_students=Count("locations")).first()
            
            if open_trip:
                location = Location.objects.create(
                        name = form.cleaned_data['name'],
                        faculty = student_faculty,
                        trip = open_trip
                )
            else:
                new_trip = Trip.objects.create(status=Status.OPEN)
                location = Location.objects.create(
                        name = form.cleaned_data['name'],
                        faculty = student_faculty,
                        trip = new_trip
                )

            # location = form
            # location.trip = open_trip  
                    
            location.trip.save()
            # location.save()
            trip = location.trip
            # grouped_list = Location.objects.values('faculty').annotate(count=Count('pk'))
            sent = False
            # for faculties in grouped_list:
            if trip.locations.count() == 3:
                trip.mark_full()
                trip.save()

                send_mail('Notification', 'You have a list of people', 'khaleedsemilore@gmail.com', 
                ['khaleedalhazan@gmail.com'])
                sent = True
                trip.mark_complete()
                trip.save()
                messages.success(request, f"Your Bus Group from {student_faculty} is now Full the driver has been notified") 
                return redirect('complete')  
                
            else:
                messages.success(request, f"Your Ride is been processed, looking for others around you ")
            # messages.warning(request, f"Sign Up or Log In to Enjoy More")
            return redirect('home')
                    
    else:
        form = LocationForm()
    return render(request, 'core/location.html', {'form': form})

def open_trips(request):
    trips = Trip.objects.filter(status='Open').values('locations__faculty', 'status').annotate(num_students=Count("locations"))
    return render(request, 'core/open_trips.html', {'trips': trips})

def trip_details(request):
    return render(request, 'core/trips_details.html')


def complete(request):
    return render(request, 'core/complete.html')







"""
# THEN AND STILL EXIST #
THE REMAINING BUG IS THAT THE TRIP IS CREATED WITH OPEN AS IT'S STATUS 
BUT WITHIN THE TRIP DROPDOWN IT'S TRIP OBJECT IT'S SHWOING INSTEAD OF TRIP CHOICES
"""
"""                                               
# NOW #
THE TRIP IS CREATED WITH OPEN STATUS BUT THE LOCATION OBJECT IS NOT CREATED
THOUGH I WASN'T ABLE TO SAVE THE LOCATIONWITH JUST 'location = form.save()'
                                                                                # SOLVED #
"""
"""
THE NEW PROBLEM IS THAT THE TRIP THAT IS CREATED IS BASED ON LOCATION OBJECT AND WITH NO REFRENCES TO FACULTY 
AND WITH THAT WHEN THE NO. OF STUDENTS THAT ORDER EQUAL THRESHOLD IT WILL ACTIVATE EVEN WITH DIFFERENT FACULTY 
"""





















































































# if request.method == 'POST':
#         form = LocationForm(request.POST)
#         if form.is_valid():
#             if request.user.is_authenticated:
#                 # location_instance = form.save()

#                 open_trip = Trip.objects.filter(status=Status.OPEN).annotate(num_students=Count("locations")).first()
#                 location_instance = form.save()

#                 if open_trip:
#                     locations_instance.trip = open_trip
#                 else:
#                     new_trip = Trip.objects.create(status=Status.OPEN)
#                     locations_instance.trip = new_trip

#                 location_instance.trip.save()

#                 trip = location_instance.trip
#                 # grouped_list = Location.objects.values('faculty').annotate(count=Count('pk'))
#                 sent = False
#                 # for faculties in grouped_list:
#                 if trip.locations.count() == 3:
#                     trip.mark_full()
#                     trip.save()
#                     messages.success(request, f"Your Bus Group is now Full the driver is on his way")

#                     send_mail('Notification', 'You have a list of people', 'khaleedsemilore@gmail.com', 
#                     ['khaleedalhazan@gmail.com'])
#                     sent = True

# trip = location_instance.trip
#                 # grouped_list = Location.objects.values('faculty').annotate(count=Count('pk'))
#                 sent = False
#                 # for faculties in grouped_list:
#                 if trip.status == 'OPEN' and faculties['count'] == 3:
#                     trip.mark_full()
#                     trip.save()
#                     messages.success(request, f"Your Bus Group is now Full the driver is on his way")

#                     send_mail('Notification', 'You have a list of people', 'khaleedsemilore@gmail.com', 
#                     ['khaleedalhazan@gmail.com'])
#                     sent = True
#                     trip.mark_complete()
#                     trip.save()
#                     messages.success(request, f"Your Bus Order is now completed the driver is on his way")   
                    
#                 else:
#                     messages.success(request, f"Your Ride is been processed, looking for others around you ")   
                    
#             else:
#                 messages.warning(request, f"Sign Up or Log In to Enjoy More")
#                 return redirect('login')
#     else:
#         form = LocationForm()
#     return render(request, 'core/location.html', {'form': form})


# def complete(request):
#     return render(request, 'core/complete.html')


# def done(request):
#     return render(request, 'core/done.html')

























































# from django.shortcuts import render, redirect
# from .forms import LocationForm
# from django.contrib import messages
# from core.models import Location
# from django.core.mail import send_mail
# from django.db.models import Count


# def home(request):
#     return render(request, 'core/home.html')


# def location(request):
#     if request.method == 'POST':
#         form = LocationForm(request.POST)
#         if form.is_valid():
#             if request.user.is_authenticated:
#                 form.save()
#                 grouped_list = Location.objects.values('faculty').annotate(count=Count('pk'))
#                 sent = False
#                 for faculties in grouped_list:
#                     if faculties['count'] == 5:
#                         send_mail('Notification', 'You have a list of people', 'khaleedsemilore@gmail.com', 
#                         ['khaleedalhazan@gmail.com'])
#                         sent = True
#                         messages.success(request, f"Your Input has been submitted")   
#                         return redirect("complete")
#                     else:
#                         messages.success(request, f"Your Input has been submitted")   
#                         return redirect("done")
#             else:
#                 messages.warning(request, f"Sign Up or Log In to Enjoy More")
#                 return redirect('login')
#     else:
#         form = LocationForm()
#     return render(request, 'core/location.html', {'form': form})


# def complete(request):
#     return render(request, 'core/complete.html')


# def done(request):
#     return render(request, 'core/done.html')
