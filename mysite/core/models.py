from django.db import models


class Photo(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    # upload_to -> okreslenie directory
    pdf = models.FileField(upload_to='photos/pdfs/')
    original = models.ImageField(upload_to='photos/original/', null=True, blank=True)

    def __str__(self):
        return self.title

    # function which deletes files (that were save) from PC
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.original.delete()
        super().delete(*args, **kwargs)