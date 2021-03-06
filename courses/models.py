from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_better_admin_arrayfield.models.fields import ArrayField

class Course(models.Model):

    class Meta:
        verbose_name_plural = "courses"
    
    title = models.CharField(_('title'),help_text=_('Ex: c++ Introduction'), max_length=255,blank=False)
    links = ArrayField(verbose_name=_('please add link'),base_field=models.URLField(),blank=True,help_text=_('Ex: https://www.site.com/something.pdf'),null=True)
    note = models.TextField(_('note'),help_text=_('some additional note'),blank=True,null=True)
    description = models.TextField(_('description'),help_text=_('some description'),blank=False)
    tags = ArrayField(verbose_name=_('please add tag'),base_field=models.TextField(),blank=True,help_text=_('Ex: Arduino'),null=True)
    requirements = models.ManyToManyField(to='self',verbose_name='requirements',blank=True)

    REQUIRED_FIELDS = ['title','price','currency','description','teacher','dates']

    def __str__(self):
        return 'TITLE:%s ID:%s' % (self.title,self.id)

    def find(self,keywords):
        return self.objects.filter(title__contains=keywords)

class CourseDate(models.Model):

    class Currencies(models.TextChoices):
        HTG = 'HTG', _("HTG")

    class Meta:
        verbose_name_plural = "Course Dates"
        get_latest_by = 'date' #max_rated_entry = YourModel.objects.latest()

    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    price = models.DecimalField(_('price'),help_text=_('Ex: 1000'),max_length=255,max_digits=11,decimal_places=2,blank=False,default=1000)
    currency = models.CharField(_('currency'),max_length=25,choices=Currencies.choices,default=Currencies.HTG,blank=False)
    course = models.ForeignKey(verbose_name=_('course'),to='Course',on_delete=models.CASCADE)
    date = models.DateTimeField(_('date'),max_length=255,blank=False)
    nb_attendees = models.IntegerField(_('number of attendees'),help_text=_('Ex: 50'),blank=False)
    attendees = models.ManyToManyField(to=get_user_model(),through='Attendee',through_fields=('date','attendee'),related_name='attendees',blank=True)
    
    REQUIRED_FIELDS = ['course','nb_attendees','date','attendees']

    def __str__(self):
        return 'COURSE:%s  DATE:%s' % (self.course,self.date)

    def remain(self):
        return self.objects.nb_attendees - self.objects.attendees.all().count()

    def populars(self):
        return self.objects.annotate(attendee_count=models.Count('attendees')).filter(attendee_count__gte=5) #base on people num


class Attendee(models.Model):

    class Meta:
        verbose_name_plural = "Attendees"

    date = models.ForeignKey(verbose_name=_('date'),to='CourseDate', on_delete=models.CASCADE)
    attendee = models.ForeignKey(verbose_name=_('attendee'),to=get_user_model(), on_delete=models.CASCADE)
    complete = models.BooleanField(verbose_name=_('complete'),blank=False,default=False)
    score = models.DecimalField(_('score'),help_text=_('Ex: 18.5'),max_length=255,max_digits=11,decimal_places=2,blank=False,default=0)

    REQUIRED_FIELDS = ['date','attendee','score','complete']

    def __str__(self):
        return 'DATE:%s  ATTENDEE:%s' % (self.date.id,self.attendee.id)
