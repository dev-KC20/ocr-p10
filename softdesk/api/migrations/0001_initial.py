# Generated by Django 4.0.4 on 2022-05-30 14:24

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contributor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("A", "Auteur"), ("M", "Membre")], default="M", max_length=1)),
                (
                    "permission",
                    models.CharField(
                        choices=[
                            ("C", "Créer"),
                            ("R", "Lire"),
                            ("CR", "Créer et Lire"),
                            ("CRUD", "Créer, Lire, Actualiser, Supprimer"),
                        ],
                        default="C",
                        max_length=4,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=48)),
                ("description", models.CharField(max_length=516)),
                (
                    "type",
                    models.CharField(
                        choices=[("B", "Back-end"), ("F", "Front-end"), ("I", "IOS"), ("A", "Android")],
                        default="F",
                        max_length=1,
                    ),
                ),
                (
                    "author_users",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.SET(api.models.get_sentinel_user),
                        related_name="project_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("contributors", models.ManyToManyField(through="api.Contributor", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=48)),
                ("description", models.CharField(max_length=516)),
                (
                    "tag",
                    models.CharField(
                        choices=[("B", "Bug"), ("I", "Amélioration"), ("T", "Tâche")], default="T", max_length=1
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("1", "Faible"), ("2", "Moyenne"), ("3", "Elevé")], default="1", max_length=1
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("1", "À faire"), ("2", "En cours"), ("3", "Terminé")], default="1", max_length=1
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "assignee_user",
                    models.ForeignKey(
                        on_delete=models.SET(api.models.get_sentinel_user),
                        related_name="issue_assignee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "author_user",
                    models.ForeignKey(
                        on_delete=models.SET(api.models.get_sentinel_user),
                        related_name="issue_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="api.project")),
            ],
        ),
        migrations.AddField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributor_project",
                to="api.project",
            ),
        ),
        migrations.AddField(
            model_name="contributor",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET(api.models.get_sentinel_user),
                related_name="contributor_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=516)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "author_user",
                    models.ForeignKey(
                        on_delete=models.SET(api.models.get_sentinel_user),
                        related_name="comment_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("issue", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="api.issue")),
            ],
        ),
    ]
