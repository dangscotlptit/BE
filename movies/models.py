from djongo import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()
    poster_url = models.URLField(blank=True)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title
