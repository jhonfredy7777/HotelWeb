from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .models import Reservation,Customer,Room,ContactMessage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import date

# Create your views here.

def home(request):
    return render(request,"index.html",{})


def rooms_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    available_filter = request.GET.get('available', '')
    sort_by = request.GET.get('sort_by', 'number')

    rooms= Room.objects.all()
    # Filter by number
    if search_query:
        rooms = rooms.filter(number__icontains=search_query)  
    
    # Filter rooms according to parameters
    if category_filter:
        rooms = rooms.filter(category=category_filter)
    if available_filter == 'true':  
        rooms = rooms.filter(available=True)
    elif available_filter == 'false':  
        rooms = rooms.filter(available=False)

    # Apply ordering
    if sort_by == 'price':
        rooms = rooms.order_by('price')  
    else:
        rooms = rooms.order_by('number')    

    # Pagination (12 rooms for page)
    paginator = Paginator(rooms, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reservation/rooms_list.html', {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'available_filter': available_filter,
        'sort_by': sort_by,
        'search_query': search_query
    })


def room_detail(request,number):
    room = get_object_or_404(Room, number=number)
    return render(request,'reservation/room_detail.html',{'room': room})

@login_required
def book_room(request,number):
    room = get_object_or_404(Room, number=number)
    # Validation: if room not available, redirect with an error
    if not room.available:
        messages.error(request, "This room is not available at the moment.")
        return redirect('Room_detail', number)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        exp_date = request.POST.get('exp_date', '').strip()
        cvv = request.POST.get('cvv', '').strip()

        # basic Validations
        if not full_name or not email or not date or not time or not card_number or not exp_date or not cvv:
            messages.error(request, "All fields are required.")
            return render(request, 'reservation/book_room.html', {
    'room': room,
    'form_data': {
        'full_name': full_name,
        'email': email,
        'date': date,
        'time': time,
        'card_number': card_number,
        'exp_date': exp_date,
        'cvv': cvv,
    }
})


        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Email is not valid.")
            return render(request, 'reservation/book_room.html', {
    'room': room,
    'form_data': {
        'full_name': full_name,
        'email': email,
        'date': date,
        'time': time,
        'card_number': card_number,
        'exp_date': exp_date,
        'cvv': cvv,
    }
})


        # Validate card number
        if not card_number.isdigit() or len(card_number) not in [13, 16]:
            messages.error(request, "Card number no valid.")
            return render(request, 'reservation/book_room.html', {
    'room': room,
    'form_data': {
        'full_name': full_name,
        'email': email,
        'date': date,
        'time': time,
        'card_number': card_number,
        'exp_date': exp_date,
        'cvv': cvv,
    }
})


        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            messages.error(request, "CVV code no valid.")
            return render(request, 'reservation/book_room.html', {
    'room': room,
    'form_data': {
        'full_name': full_name,
        'email': email,
        'date': date,
        'time': time,
        'card_number': card_number,
        'exp_date': exp_date,
        'cvv': cvv,
    }
})


        # if everything is okay
        # get or Create customer
        customer, created = Customer.objects.get_or_create(
    user=request.user,
    defaults={'full_name': request.user.username, 'email': request.user.email}
)

        #  Create reservation
        Reservation.objects.create(
            room=room,
            customer=customer,
            date=date,
            time=time,
            state='confirmed',
            paid=True,
            res_email=email,
            behalf_of=full_name,
        )
        # Label room as no available
        room.available = False
        room.save()
        # send email
        subject = 'Room Reservation Confirmed'
        from_email = 'Info@solymar.com'
        destination_list=[request.user.email,email]

        html_content = render_to_string('emails/booking_confirmation.html', {'full_name':full_name,'room':room,'date':date,'time':time})
        text_content = f"""Hello {full_name}, 
Your reservation for room {room.number} is confirmed for {date} at {time}.
Thank you!
"""

        msg = EmailMultiAlternatives(subject, text_content, from_email, destination_list )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "You're playment was received. Room booked successfully. Check your email, we sent all the information there.")
        return redirect("Room_detail", number) 
    return render(request,'reservation/book_room.html',{'room': room})


@login_required
def book_room_free(request,number):
    room = get_object_or_404(Room, number=number)
    # Validation: if room not available, redirect with an error
    if not room.available:
        messages.error(request, "This room is not available at the moment.")
        return redirect('Room_detail', number)
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()

        # basic Validations
        if not full_name or not email or not date or not time :
            messages.error(request, "All fields are required.")
            return render(request, 'reservation/book_room_free.html', {
    'room': room,
    'form_data': {
        'full_name': full_name,
        'email': email,
        'date': date,
        'time': time,
        
    }
})
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Email is not valid.")
            return render(request, 'reservation/book_room_free.html', {
    'room': room,
    'form_data': {
        'full_name': full_name,
        'email': email,
        'date': date,
        'time': time,
        
    }
})
        
        # if everything is okay
        # get or Create customer
        customer, created = Customer.objects.get_or_create(
    user=request.user,
    defaults={'full_name': request.user.username, 'email': request.user.email}
)
        
        #  Create reservation
        Reservation.objects.create(
            room=room,
            customer=customer,
            date=date,
            time=time,
            state='confirmed',
            res_email=email,
            behalf_of=full_name,
        )
        # Label room as no available
        room.available = False
        room.save()
        # send email
        subject = 'Room Reservation Confirmed'
        from_email = 'Info@solymar.com'
        destination_list=[request.user.email,email]

        html_content = render_to_string('emails/booking_free_confirmation.html', {'full_name':full_name,'room':room,'date':date,'time':time})
        text_content = f"""Hello {full_name}, 
Your reservation for room {room.number} is confirmed for {date} at {time}.
Thank you!
"""  

        msg = EmailMultiAlternatives(subject, text_content, from_email, destination_list )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Room booked successfully. Check your email, we sent all the information there.")
        return redirect("Room_detail", number)
    return render(request,'reservation/book_room_free.html',{'room': room})

@login_required
def cancel_reservation(request, code):
    reservation = get_object_or_404(Reservation, res_code=code, customer__user=request.user)

    if reservation.status == 'cancelled':
        messages.info(request, "This reservation is already cancelled.")
        return redirect('Customer_reservations')

    # Check if the reservation date has already passed
    if reservation.date < date.today():
        messages.error(request, "You cannot cancel a reservation that has already passed.")
        return redirect('Customer_reservations')
    
    

    # Change reservation status and room availability
    reservation.status = 'cancelled'
    reservation.save()

    reservation.room.available = True
    reservation.room.save()

    # send email
    subject = 'Room Reservation Cancelled'
    from_email = 'Info@solymar.com'
    destination_list=[request.user.email,reservation.res_email]

    html_content = render_to_string('emails/cancelation_email.html', {'full_name':reservation.behalf_of,'room':reservation.room,'date':reservation.date,'time':reservation.time})
    text_content = f"""Hello {reservation.behalf_of}, 
Your reservation for room {reservation.room.number} for {reservation.date} at {reservation.time} is cancelled.
Thank you. We look forward to host you again!
"""

    msg = EmailMultiAlternatives(subject, text_content, from_email, destination_list )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    messages.success(request, "Your reservation has been cancelled.")
    return redirect('Customer_reservations')




# @login_required
# def make_reservation(request):
#     if request.method == "POST":
#         date = request.POST.get("date")
#         time = request.POST.get("time")
#         Reservation.objects.create(user=request.user, date=date, time=time, state="Pending")
#         return JsonResponse({"message": "Reservation created succesfully"}, status=200)
#     return render(request, "reservas/make_reservation.html")

def about_us(request):
    return render(request,"about_us.html",{})


def hotel_activities(request):
    return render(request,"hotel_activities.html",{})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # basic Validations
        if not name or not email or not message or not subject :
            messages.error(request, "All fields are required.")
            return render(request, 'contact/contact.html', {
    
    'form_data': {
        'name': name,
        'email': email,
        'message': message,
        'subject':subject,
        
    }
})
        
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Email is not valid.")
            return render(request, 'contact/contact.html', {
    'form_data': {
        'name': name,
        'email': email,
        'message': message,
        'subject':subject,
        
    }
})
        # save contact message
        ContactMessage.objects.create(
            full_name=name,
            email=email,
            subject=subject,
            message=message,
        )
        # send email notification
    
        subject = 'Thank you for reaching out to us'
        from_email = 'Info@solymar.com'
        destination_list=[email]

        html_content = render_to_string('emails/thankyou_email.html',{'name':name})
        text_content = f"""Hello, {name}.\nYour message has been successfully sent. We appreciate you reaching out to us.\n
Our team will get back to you as soon as possible. If your inquiry is urgent, please feel free to call us directly.\n
Thank you!
"""  

        msg = EmailMultiAlternatives(subject, text_content, from_email, destination_list )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return render(request,'contact/thank_you.html')

    return render(request,"contact/contact.html",{})

