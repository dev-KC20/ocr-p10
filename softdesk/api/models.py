from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# from users.models import User

# for RGPD & others reasons when a contributor is deleted one want to keep projects, issues or comments


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deletedUser')[0]


class Project(models.Model):

    BACK = 'B'
    FRONT = 'F'
    IOS = 'I'
    ANDROID = 'A'
    PROJECT_TYPE_CHOICES = [
        (BACK, 'Back-end'),
        (FRONT, 'Front-end'),
        (IOS, 'IOS'),
        (ANDROID, 'Android'),
    ]
    author_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', )
    # How you qualify its this project
    title = models.CharField(max_length=48, blank=False, null=False)
    # How you describe what this project is
    description = models.CharField(max_length=516, blank=False, null=False)
    # What type of infrastruture the project is about
    type = models.CharField(blank=False, null=False,
                            max_length=1,
                            choices=PROJECT_TYPE_CHOICES,
                            default=FRONT,
                            )

    def __str__(self):
        return title


class Issue(models.Model):

    BUG = 'B'
    IMPROVEMENT = 'I'
    TASK = 'T'
    ISSUE_TAG_CHOICES = [
        (BUG, 'Bug'),
        (IMPROVEMENT, 'Amélioration'),
        (TASK, 'Tâche'),
    ]

    LOW = '1'
    MEDIUM = '2'
    HIGH = '3'
    ISSUE_PRIORITY_CHOICES = [
        (LOW, 'Faible'),
        (MEDIUM, 'Moyenne'),
        (HIGH, 'Elevé'),
    ]

    OPEN = '1'
    IN_PROGRESS = '2'
    CLOSED = '3'
    ISSUE_STATUS_CHOICES = [
        (OPEN, 'À faire'),
        (IN_PROGRESS, 'En cours'),
        (CLOSED, 'Terminé'),
    ]

    # if the project gets deleted then also its issues
    project = models.ForeignKey(Project,  on_delete=models.CASCADE,)
    # if the contributor gets deleted then this issue author_user record becomes 'sentinel_user' named here deleted
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_author',
                                    on_delete=models.SET(get_sentinel_user),)
    # if the contributor gets deleted then this issue assignee_user record becomes 'sentinel_user' named here deleted
    assignee_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      related_name='issue_assignee',  on_delete=models.SET(get_sentinel_user),)
    # How you qualify its this issue
    title = models.CharField(max_length=48, blank=False, null=False)
    # How you describe what this issue is
    description = models.CharField(max_length=516, blank=False, null=False)
    # What nature of issue we're dealing with
    tag = models.CharField(blank=False, null=False,
                           max_length=1,
                           choices=ISSUE_TAG_CHOICES,
                           default=TASK,
                           )
    # What pritoty, not urge the issue has for the contributor
    priority = models.CharField(blank=False, null=False,
                                max_length=1,
                                choices=ISSUE_PRIORITY_CHOICES,
                                default=LOW,
                                )
    # What status the issue is in
    status = models.CharField(blank=False, null=False,
                              max_length=1,
                              choices=ISSUE_STATUS_CHOICES,
                              default=OPEN,
                              )

    # A timestamp representing when this object was created.
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return title



class Comment(models.Model):

    # if the issue gets deleted then also its comment
    issue = models.ForeignKey(Issue,  on_delete=models.CASCADE,)
    # if the contributor gets deleted then this comment author_user record becomes 'sentinel_user' named here deleted
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_author',
                                    on_delete=models.SET(get_sentinel_user),)
    # How you describe what this issue is
    description = models.CharField(max_length=516, blank=False, null=False)
    # A timestamp representing when this object was created.
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return description

class Contributor(models.Model):
    CREATE = 'C'
    READ = 'R'
    UPDATE = 'U'
    DELETE = 'D'
    PROJECT_PERMISSION_CHOICES = [
        (CREATE, 'Créer'),
        (READ, 'Lire'),
        (UPDATE, 'Actualiser'),
        (DELETE, 'Supprimer'),
    ]
    OWNER = 'O'
    AUTHOR = 'A'
    MEMBER = 'M'

    PROJECT_ROLE_CHOICES = [
        (OWNER, 'Responsable'),
        (AUTHOR, 'Auteur'),
        (MEMBER, 'Membre'),
    ]

    # if the user gets deleted then contributor becomes 'sentinel_user' named here deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.SET(get_sentinel_user),)
    # if the project gets deleted then delete Contributor
    project = models.ForeignKey(Project,  on_delete=models.CASCADE, null=True)
    role = models.CharField(
        max_length=1,
        choices=PROJECT_ROLE_CHOICES,
        default=MEMBER,
    )
    permission = models.CharField(
        max_length=1,
        choices=PROJECT_PERMISSION_CHOICES,
        default=READ,
    )

    class Meta:
        models.UniqueConstraint(fields=['user', 'project', 'role'], name='unique__role__for__user__in_project')

        def __str__(self):
            return str(user.email) + (project.title) + role