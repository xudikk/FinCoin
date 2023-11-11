from django.db import models

from core.models import User


class Chat(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    desc = models.CharField(max_length=1028, null=True, blank=True)
    chat_type = models.IntegerField(default=1, choices=((1, "Lichniy Chat"), (2, "Gruppa"),))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.id} // {self.created}"

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chatlar"


class ChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "ChatUser"
        verbose_name_plural = "ChatUsers"

    def __str__(self):
        return f"{self.user} // {self.chat.id}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    media = models.FileField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.chat.id} // {self.message if self.message else ''} // {self.user}"


class Reply_Message(models.Model):
    repliedMessage = models.ForeignKey(Message, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    media = models.FileField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Reply_Message"
        verbose_name_plural = "Reply_Messages"

    def __str__(self):
        return f"{self.message}  => {self.repliedMessage}"


class ViewMessages(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    isView = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.user} // {self.isView}"

    class Meta:
        verbose_name = "View Message"
        verbose_name_plural = "View Messages"
