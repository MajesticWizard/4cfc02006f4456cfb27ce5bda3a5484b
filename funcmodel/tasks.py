import random
import string
import os
import time
import matplotlib.pyplot as plt
from django.utils import timezone
from numexpr import evaluate
import numpy as np
from django.conf import settings
from main.celery import app
from .models import Function


@app.task
def update_plot(id):

    obj = Function.objects.get(id=id)
    obj.processed = timezone.now()

    try:
        function = str(obj.signature).replace("^", "**")
        upper_limit = int(time.mktime(obj.processed.timetuple()))
        lower_limit = upper_limit - int(obj.interval) * 86400
        t = np.arange(lower_limit, upper_limit, int(obj.steep) * 3600, dtype=np.float64)
        y = evaluate(function)

        fig, ax = plt.subplots()
        ax.plot(t, y)
        ax.set(xlabel='time (s)')
        ax.grid()
        #plt.axis([t.min(), t.max(), y.min(), y.max()])

        if str(obj.plot) != '':
            os.remove(settings.MEDIA_ROOT + str(obj.plot))

        obj.plot = ''.join(random.choice(string.ascii_letters) for _ in range(15)) + ".png"
        fig.savefig(settings.MEDIA_ROOT + str(obj.plot))
        obj.save()

    except Exception as e:
        obj.plot = str(e)
        obj.save()
