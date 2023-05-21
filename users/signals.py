from django.db.models.signals import post_save , pre_save
from django.db.models import Avg
from django.dispatch import receiver
from django.conf import settings
from django.core.files import File
from .logs import log

from .models import Doctor, DocViews, RatingSystem


from rest_framework.authtoken.models import Token
from io import BytesIO
from PIL import Image, ImageDraw
import qrcode

@receiver(pre_save,sender=Doctor)
def save(sender,**kwargs):
        dview = kwargs['instance']
        view = DocViews.objects.filter(doc=dview)
        dview.views = view.count()

        rate = RatingSystem.objects.filter(doctor=dview).aggregate(rate__avg=Avg('rate'))
        exist_rate = rate['rate__avg']
        dview.avgRating = rate['rate__avg']
        if exist_rate is None:
            dview.avgRating = 0.00


@receiver(post_save, sender=Doctor)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_auth_token(sender, instance=None, created=False, **kwargs):
    user = instance
    if created:
        token = Token.objects.create(user=instance)
        log(message=token)
        qrcode_img=qrcode.make(user.otp)
        canvas=Image.new("RGB", (300,300),"white")
        draw=ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer=BytesIO()
        canvas.save(buffer,"PNG")
        user.qrcode.save(f'qrcode{user.pk}.png',File(buffer))
        canvas.close()




