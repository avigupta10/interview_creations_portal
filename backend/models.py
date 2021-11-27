from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Interviewer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Interview(models.Model):
    candidate_name = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interviewer_name = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='media/', blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.candidate_name.name
