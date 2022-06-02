# Generated by Django 4.0.4 on 2022-06-02 18:08

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='author_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(api.models.get_sentinel_user), related_name='project_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(through='api.Contributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee_user',
            field=models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_user), related_name='issue_assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='author_user',
            field=models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_user), related_name='issue_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributor_project', to='api.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(api.models.get_sentinel_user), related_name='contributor_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='author_user',
            field=models.ForeignKey(on_delete=models.SET(api.models.get_sentinel_user), related_name='comment_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.issue'),
        ),
    ]
