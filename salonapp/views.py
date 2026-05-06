from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import User,Service,Booking,StaffService,Staff
from datetime import datetime, date ,timedelta

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)

            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == 'admin':
                return redirect('admin_home')
            elif user.role == 'staff':
                return redirect('staff_home')
            else:
                return redirect('view_services')

        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')
from django.shortcuts import render, redirect
from .models import User  # your custom User table

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # ✅ Password match check
        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        # ✅ Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        
        User.objects.create(
            username=username,
            email=email,
            password=password,
            role='customer'
        )

        return redirect('login')  # go to login page after register

    return render(request, 'register.html')
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']   # remove session

    return redirect('home')  # redirect to login page
def home(request):
    services = Service.objects.all()  # fetch all services
    return render(request, 'home.html', {'services': services})

def admin_home(request):
    if request.session.get('role') != 'admin':
        return redirect('login')
    return render(request, 'admin_home.html')





def customer_home(request):
   
    services = Service.objects.all()
    return render(request, 'customer_home.html', {'services': services})

def service_detail(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'service_detail.html', {'service': service})



def generate_slots(service, selected_date):
    start_time = datetime.strptime("09:30", "%H:%M")
    end_time = datetime.strptime("20:30", "%H:%M")

    duration = service.duration  # in minutes
    slots = []

    current = start_time

    while current + timedelta(minutes=duration) <= end_time:
        slot_time = current.time()

        # Check if already booked
        if not Booking.objects.filter(date=selected_date, time=slot_time).exists():
            slots.append(slot_time)

        current += timedelta(minutes=duration)

    return slots

from django.shortcuts import render, redirect

def book_service(request, id):
    

    if not request.session.get('user_id'):
        return redirect(f'/login/?next=/book_service/{id}/')

    if request.session.get('role') != 'customer':
        return redirect('login')

    service = Service.objects.get(id=id)
    slots = []
    selected_date = None
    

    if request.method == 'POST':
        
        selected_date_str = request.POST.get('date')  # always keep it

        selected_time = request.POST.get('time')

        if selected_date_str:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

            if selected_date < date.today():
                return render(request, 'book_service.html', {
                    'service': service,
                    'error': 'Cannot select past date',
                    'today': date.today()
                })

            slots = generate_slots(service, selected_date)
    
        if selected_time and selected_date_str:
            selected_time = selected_time.lower().replace('a.m.', '').replace('p.m.', '').strip()
            selected_time = datetime.strptime(selected_time, '%H:%M').time()

            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

            if Booking.objects.filter(date=selected_date, time=selected_time).exists():
                return render(request, 'book_service.html', {
                    'service': service,
                    'slots': slots,
                    'selected_date': selected_date,
                    'error': 'Slot already booked',
                    'today': date.today()
                })
            staff_user = StaffService.objects.filter(service=service).first().staff
            Booking.objects.create(
                customer_id=request.session['user_id'],
                staff=staff_user,
                service=service,
                date=selected_date,
                time=selected_time
            )
        
            return redirect('my_bookings')

    return render(request, 'book_service.html', {
        'service': service,
        'slots': slots,
        'selected_date': selected_date,
        'today': date.today()
    })
def my_bookings(request):
    if 'user_id' not in request.session or request.session.get('role') != 'customer':
        return redirect('login')

    user_id = request.session['user_id']

    bookings = Booking.objects.filter(customer_id=user_id)

    return render(request, 'my_bookings.html', {'bookings': bookings})

def add_service(request):
    if request.session.get('role') != 'admin':
        return redirect('login')
    staff_list = User.objects.filter(role='staff')

    if request.method == 'POST':
        name = request.POST.get('service_name')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        staff_id = request.POST.get('staff')

        service=Service.objects.create(
            service_name=name,
            price=price,
            duration=duration,
            description=description
        )
        staff = User.objects.get(id=staff_id)

        StaffService.objects.create(
            staff=staff,
            service=service
        )

        return redirect('admin_view_services')

    return render(request, 'add_services.html', {'staff_list': staff_list})

def view_services(request):
    services = Service.objects.all()
    

    return render(request, 'view_services.html', {'services': services})
def edit_service(request, id):
    service = Service.objects.get(id=id)

    if request.method == 'POST':
        service.service_name = request.POST['service_name']
        service.price = request.POST['price']
        service.duration = request.POST['duration'] 
        service.description = request.POST['description']
        service.save()
        return redirect('admin_view_services')

    return render(request, 'edit_service.html', {'service': service})


def delete_service(request, id):
    service = Service.objects.get(id=id)
    service.delete()
    return redirect('admin_view_services')

def add_staff(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')
        experience = request.POST.get('experience')

        
        user = User.objects.create(
            username=username,
            password=password,
            role='staff'
        )

        
        Staff.objects.create(
            user=user,
            email=email,
            phone=phone,
            service_type=service_type,
            experience=experience if experience else None
        )

        return redirect('admin_home')

    return render(request, 'add_staff.html')

def view_customers(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    customers = User.objects.filter(role='customer')
    return render(request, 'view_customers.html', {'customers': customers})

def view_staff(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    staff = User.objects.filter(role='staff')
    return render(request, 'view_staff.html', {'staff': staff})
def admin_view_services(request):
   
    if request.session.get('role') != 'admin':
        return redirect('login')

    services = Service.objects.all()

    return render(request, 'admin_view_services.html', {
        'services': services
    })


def staff_home(request):
    if 'user_id' not in request.session:
        return redirect('login')

    # get logged-in staff user
    staff = User.objects.get(
        id=request.session['user_id'],
        role='staff'
    )

    # fetch only bookings assigned to this staff
    bookings = Booking.objects.filter(
        staff=staff
    ).order_by('-date', '-time')

    return render(request, 'staff_home.html', {
        'bookings': bookings,
        'staff': staff,
        'today': date.today()
    })
def complete_booking(request, id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=id)

        # OPTIONAL security (recommended)
        if request.session.get('role') != 'staff':
            return redirect('login')

        # Update status
        booking.status = 'Completed'
        booking.save()

    return redirect('staff_home')