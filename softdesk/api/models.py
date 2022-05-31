from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def get_sentinel_user():
    # for RGPD & others reasons when a contributor is deleted one want to keep projects, issues or comments
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
    # author is the owner of the project
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_owner', blank=True, null=True,
                                     on_delete=models.SET(get_sentinel_user),)
    # list of the members of the projets is held in external Contributor model
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          through='Contributor',
                                        #   through_fields=('project', 'user'),
                                           )
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
        return self.title


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
        return self.title


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
        return self.description


class Contributor(models.Model):
    # so far only 4 combinations of basic CRUD rights
    CREATE = 'C'
    READ = 'R'
    CREATE_READ = 'CR'
    CREATE_READ_UPDATE_DELETE = 'CRUD'
    PROJECT_PERMISSION_CHOICES = [
        (CREATE, 'Créer'),
        (READ, 'Lire'),
        (CREATE_READ, 'Créer et Lire'),
        (CREATE_READ_UPDATE_DELETE, 'Créer, Lire, Actualiser, Supprimer'),
    ]

    # a project owner is a project author
    AUTHOR = 'A'
    MEMBER = 'M'
    PROJECT_ROLE_CHOICES = [
        (AUTHOR, 'Auteur'),
        (MEMBER, 'Membre'),
    ]

    # if the user gets deleted then contributor becomes 'sentinel_user' named here deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', related_name="contributor_user",
                             blank=True, null=True,  on_delete=models.SET(get_sentinel_user),)
    # if the project gets deleted then delete Contributor
    project = models.ForeignKey(Project, to_field='id', related_name="contributor_project",
                                on_delete=models.CASCADE, null=True)

    role = models.CharField(
        max_length=1,
        choices=PROJECT_ROLE_CHOICES,
        default=MEMBER,
    )
    # the permission field is more for information than driving the api rights behavior
    permission = models.CharField(
        max_length=4,
        choices=PROJECT_PERMISSION_CHOICES,
        default=CREATE,
    )

    class Meta:
        models.UniqueConstraint(fields=['user', 'project', ], name='user__once__in_project')

    def __str__(self):
        return str(self.user.email) + ' on '  + (self.project.title)+ ' as '  + self.role
