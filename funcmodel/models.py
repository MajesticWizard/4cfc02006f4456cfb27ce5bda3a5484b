from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from os import remove
from PIL import Image


class Function(models.Model):
    signature = models.CharField(max_length=150, verbose_name='Function')
    plot = models.ImageField(upload_to='plots/', verbose_name='Plot', editable=False, blank=True)
    interval = models.PositiveIntegerField(default=1, verbose_name='Interval t, in days')
    steep = models.PositiveIntegerField(default=1, verbose_name='Steep dt, in hours')
    processing = models.DateTimeField(editable=False, verbose_name='Processed at', blank=True, auto_now_add=True)



    def plot_img(self):
        try:
            Image.open(settings.MEDIA_ROOT + str(self.plot))
            return mark_safe(f'<img src={settings.MEDIA_URL + str(self.plot)} style="width: 640px; height:480px;"/>')
        except:
            return str(self.plot)

    def delete(self, *args, **kwargs):
        try:
            remove(settings.MEDIA_ROOT + str(self.plot))
        except:
            pass
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-processing']
