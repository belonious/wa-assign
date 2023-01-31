from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for movierama-wa.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    opinions = models.ManyToManyField(User, related_name='movies', through='Opinion')

    def __str__(self):
        return self.title


class Opinion(models.Model):
    like = models.BooleanField()
    user = models.ForeignKey(User, related_name='u_opinions', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='m_opinions', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name='unique user movie')
        ]

    def __str__(self):
        return '{} for {}'.format(self.user, self.movie)
