from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import InterestMessage, ChatMessage
from django.http import JsonResponse
from django.db.models import Q

# Function to register a new user.
# Handles user registration, checks for unique usernames, and creates a new user if valid.
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirmPassword']
        if password1 == password2:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", context={"message": "The username already exists"})
            else:
                # Create a new user
                User.objects.create_user(username=username, password=password1, email=email)
                return redirect('login')
        else:
            # Passwords do not match
            return render(request, "register.html", context={"message": "Passwords do not match"})
    return render(request, 'register.html')

# Function to log in the user.
# Handles user authentication and redirects to the home page upon successful login.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

# Home dashboard view.
# Accessible only to logged-in users. Displays a list of other users and their interest statuses.
@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current logged-in user
    # Get all interests where the current user is either the sender or recipient
    all_interests = InterestMessage.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).values('sender_id', 'recipient_id', 'accepted', 'rejected')
    
    interests_dict = {}
    for interest in all_interests:
        other_user_id = interest['recipient_id'] if interest['sender_id'] == request.user.id else interest['sender_id']
        interests_dict[other_user_id] = interest
    
    return render(request, 'home.html', {'users': users, 'sent_interests': interests_dict})

# Function to send an interest message.
# Allows a logged-in user to send an interest message to another user, if not already sent.
@login_required
def send_interest(request, recipient_id):
    if request.method == 'POST':
        recipient = get_object_or_404(User, pk=recipient_id)
        exist = InterestMessage.objects.filter(sender=request.user, recipient=recipient).exists()
        if not exist:
            message = request.POST.get('message', 'Interest')
            interest = InterestMessage(sender=request.user, recipient=recipient, message=message)
            interest.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'exists'})
    return JsonResponse({'status': 'failed'}, status=400)

# Function to retrieve received interests.
# Provides a list of interest messages received by the logged-in user that are not yet accepted or rejected.
@login_required
def received_interests(request):
    interests = InterestMessage.objects.filter(recipient=request.user, accepted=False, rejected=False)
    interests_data = [{'id': interest.id, 'sender': {'username': interest.sender.username}} for interest in interests]
    return JsonResponse({'interests': interests_data})

# Function to accept an interest message.
# Marks an interest message as accepted and redirects to the home page.
@login_required
def accept_interest(request, interest_id):
    interest = get_object_or_404(InterestMessage, pk=interest_id, recipient=request.user)
    interest.accepted = True
    interest.save()
    return redirect('home')

# Function to reject an interest message.
# Marks an interest message as rejected and redirects to the home page.
@login_required
def reject_interest(request, interest_id):
    interest = get_object_or_404(InterestMessage, pk=interest_id, recipient=request.user)
    interest.rejected = True
    interest.save()
    return redirect('home')

# Function to display the chat interface.
# Allows two users who have accepted interests to chat with each other in real-time.
@login_required
def chat(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient) | \
               ChatMessage.objects.filter(sender=recipient, recipient=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'chat.html', {'recipient': recipient, 'messages': messages})

# View to handle user logout
def user_logout(request):
    logout(request)
    return redirect('login')