from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts import models
from collections import defaultdict
from .models import Message
from .forms import MessageForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def send_message(request, recipient_username=None):
    if recipient_username:
        recipient = get_object_or_404(User, username=recipient_username)
        form = MessageForm(initial={'recipient': recipient})
    else:
        form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    return render(request, 'message/send_message.html', {'form': form})


@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-sent_at')

    conversations = {}
    unread_count = 0
    
    for message in messages:
        other_user = message.recipient if message.sender == request.user else message.sender
        if isinstance(other_user, User) and other_user.username:
            if other_user not in conversations:
                conversations[other_user] = message

            if message.recipient == request.user and not message.is_read: 
                unread_count += 1

    return render(request, 'message/inbox.html', {'conversations': conversations.items(), 'unread_count': unread_count, })

@login_required
def sent(request):
    messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    conversations = {}
    for message in messages:
        if message.recipient not in conversations:
            conversations[message.recipient] = message  

    return render(request, 'message/sent.html', {'conversations': conversations.items()})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'message/message_detail.html', {'message': message})

@login_required
def message_thread(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    messages = Message.objects.filter(
        (Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user))
    ).order_by('sent_at')

    if request.method == 'POST':
        form = MessageForm(request.POST, initial={'recipient': recipient})
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_thread', recipient_username=recipient_username)
    else:
        form = MessageForm(initial={'recipient': recipient})

    return render(request, 'message/message_thread.html', {'messages': messages, 'recipient': recipient, 'form': form})