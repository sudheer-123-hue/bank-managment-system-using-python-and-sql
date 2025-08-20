from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    price = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number}"
