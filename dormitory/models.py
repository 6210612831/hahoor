from django.db import models
from markdownx.models import MarkdownxField
from django.contrib.auth.models import User

# Create your models here.


class Review(models.Model):
    reviewto = models.OneToOneField('dormitory.Dormitory', on_delete=models.CASCADE)
    stars = models.IntegerField()
    content = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    report = models.IntegerField(default = 0)

    def __str__(self):
        return f"Reviewed {self.reviewto.title} : {self.stars} stars by {self.author}"


class Dormitory(models.Model):
    title = models.CharField(max_length=300)
    desc = models.TextField()
    content = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.IntegerField(default = 0)
    reviews = models.ManyToManyField(Review, blank=True)
    date = models.DateTimeField()
    status = models.BooleanField(default = False)
    icon = models.ImageField(upload_to='static/dormitorys/icon', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def search(self, search):
        if search.lower() in self.title.lower():
            return True
        return False
