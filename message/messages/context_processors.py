from .models import Message # type: ignore
from django.db.models import Q

def unread_messages(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(
            Q(recipient=request.user),
            Q(is_read=False)
        ).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}