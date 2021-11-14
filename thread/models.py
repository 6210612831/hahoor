from django.db import models
from markdownx.models import MarkdownxField
from django.contrib.auth.models import User
# Create your models here.


class Sub_thread(models.Model):
    replyto = models.ForeignKey('thread.Thread', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    report = models.IntegerField(default=0)

    def __str__(self):
        return f"reply {self.replyto.header} @{self.date} by {self.author}"

    class Meta:
        ordering = ['date']


class Thread(models.Model):
    header = models.CharField(max_length=300)
    content = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    report = models.IntegerField(default=0)
    reply = models.ManyToManyField(Sub_thread, blank=True)

    def __str__(self):
        return f"{self.header} by {self.author}"

    def number_reply(self):
        return self.reply.count()

    def search(self, search):
        if search.lower() in self.header.lower():
            return True
        return False

    class Meta:
        ordering = ['-date']
