from django.db.models.signals import m2m_changed

from .models import ChatChannel
from backend.lib.signal_handlers import m2m_changed_subscription

m2m_changed.connect(
    m2m_changed_subscription,
    sender=ChatChannel.messages.through,
    dispatch_uid='chat.ChatChannel_m2m_changed_subscription',
)
