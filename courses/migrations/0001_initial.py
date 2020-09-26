# Generated by Django 3.1 on 2020-09-25 22:03

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.BooleanField(default=False, verbose_name='complete')),
                ('score', models.DecimalField(decimal_places=2, default=0, help_text='Ex: 18.5', max_digits=11, max_length=255, verbose_name='score')),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='attendee')),
            ],
            options={
                'verbose_name_plural': 'Attendees',
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Ex: c++ Introduction', max_length=255, verbose_name='title')),
                ('price', models.DecimalField(decimal_places=2, help_text='Ex: 12.99', max_digits=11, max_length=255, verbose_name='price')),
                ('currency', models.CharField(choices=[('HTG', 'HTG')], default='HTG', max_length=25, verbose_name='currency')),
                ('nb_attendees', models.IntegerField(help_text='Ex: 50', verbose_name='number of attendees')),
                ('date', models.DateTimeField(max_length=255, verbose_name='date')),
                ('next_date', models.DateTimeField(max_length=255, verbose_name='next date')),
                ('links', django_better_admin_arrayfield.models.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=1), default=list, help_text='Ex: https://www.site.com/something.pdf', size=None, verbose_name='please add link')),
                ('note', models.TextField(blank=True, help_text='some additional note', null=True, verbose_name='note')),
                ('description', models.TextField(help_text='some description', verbose_name='description')),
                ('attendees', models.ManyToManyField(blank=True, related_name='attendees', through='courses.Attendee', to=settings.AUTH_USER_MODEL)),
                ('requirements', models.ManyToManyField(blank=True, related_name='_courses_requirements_+', to='courses.Courses', verbose_name='requirements')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.AddField(
            model_name='attendee',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courses', verbose_name='course'),
        ),
    ]