from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Service, Booking
from .forms import BookingForm, CareerApplicationForm, FranchiseInquiryForm, ContactForm

def home(request):
    return render(request, 'cleaning/home.html')

def about(request):
    return render(request, 'cleaning/about.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'cleaning/services.html', {'services': services})

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            
            # Send email notification
            subject = 'New Booking Request'
            message = f"""
            New booking request details:
            Name: {booking.name}
            Email: {booking.email}
            Phone: {booking.phone}
            Service: {booking.service}
            Date: {booking.date}
            Time: {booking.time}
            Notes: {booking.notes}
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['gocleeny@gmail.com', booking.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your booking has been submitted successfully!')
            return redirect('home')
    else:
        form = BookingForm()
    
    services = Service.objects.all()
    return render(request, 'cleaning/booking.html', {'form': form, 'services': services})

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    return render(request, 'cleaning/view_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'pending' and booking.status != 'confirmed':
        messages.error(request, 'You can only edit pending or confirmed bookings.')
        return redirect('view_bookings')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your booking has been updated successfully!')
            return redirect('view_bookings')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'cleaning/edit_booking.html', {'form': form, 'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'completed':
        messages.error(request, 'You cannot cancel a completed booking.')
        return redirect('view_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        
        # Send cancellation email
        subject = 'Booking Cancellation'
        message = f"""
        Your booking has been cancelled:
        Service: {booking.service}
        Date: {booking.date}
        Time: {booking.time}
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['gocleeny@gmail.com', booking.email],
            fail_silently=False,
        )
        
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('view_bookings')
    
    return render(request, 'cleaning/cancel_booking.html', {'booking': booking})

def careers(request):
    if request.method == 'POST':
        form = CareerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Send email notification
            subject = 'New Career Application'
            message = f"""
            New career application details:
            Name: {application.name}
            Email: {application.email}
            Phone: {application.phone}
            Experience: {application.experience}
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['gocleeny@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('careers')
    else:
        form = CareerApplicationForm()
    
    return render(request, 'cleaning/careers.html', {'form': form})

def franchise(request):
    if request.method == 'POST':
        form = FranchiseInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Send email notification
            subject = 'New Franchise Inquiry'
            message = f"""
            New franchise inquiry details:
            Name: {inquiry.name}
            Email: {inquiry.email}
            Phone: {inquiry.phone}
            Message: {inquiry.message}
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['gocleeny@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Your inquiry has been submitted successfully!')
            return redirect('franchise')
    else:
        form = FranchiseInquiryForm()
    
    return render(request, 'cleaning/franchise.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            
            # Send email notification
            subject = 'New Contact Message'
            message = f"""
            New contact message details:
            Name: {contact_msg.name}
            Email: {contact_msg.email}
            Message: {contact_msg.message}
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['gocleeny@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'cleaning/contact.html', {'form': form})

