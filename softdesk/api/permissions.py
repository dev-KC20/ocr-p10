from rest_framework.permissions import BasePermission, SAFE_METHODS  # , is_authenticated
from .models import Contributor, Project, Issue, Comment

# |   Role     | Project  | Iss/Comm. | Contrib |
# |------------|----------|-----------|---------|
# |anonymous   | Forbidden|	Forbidden |
# |authenticate|  C       |	C         |
# |contributor |  R       |	CR        |
# |author      |  [CR]UD  |	[CR]UD    | C


# 1. Only authenticated user can acces end-points.
# 2. Only contributors can Read Project, Comment or Issue of the project.
# 3. Only the author of a project manages (CRUD) new contributor(members).
# 4. Only authors can update (U) or delete (D) theirs Project, Comment or Issue.

# §1 Authentication is managed in the has_permission method of every perm class .
# authenticated users can Read all projects & dependencies they are contributor of
# any authenticated user can Create a new project & add contributor into


class ContributorReadCreateAuthorUpdateDelete(BasePermission):

    edit_delete_methods = ["PUT", "PATCH", "DELETE"]
    create_methods = ["POST"]
    read_methods = ["GET"]

    def has_permission(self, request, view):

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # here the request.user.is_authenticated

        # lookup section
        # hence check if request.user is contributor
        if view.kwargs.get('project_pk'):
            # non project level objects have url embeded with a project
            current_project_id = view.kwargs.get('project_pk')
        if obj.pk:
            current_obj_pk = obj.pk
        # get the member list for the current project
        if isinstance(obj, Project) or isinstance(obj, Issue) or isinstance(obj, Comment):
            if not view.kwargs.get('project_pk'):
                current_project_id = current_obj_pk
            project_members = Contributor.objects.filter(project=current_project_id)

        # authorise section
        # let superuser be superuser == have full access
        if request.user.is_superuser:
            return bool(request.user and request.user.is_superuser)
        # only the owner of one object is permitted ti Update or Delete it
        if request.method in self.edit_delete_methods:
            if isinstance(obj, Contributor):
                return True
            else:
                return obj.author_user == request.user
        elif request.method in self.create_methods:
            # authenticated user is allowed to create a new project
            if isinstance(obj, Project):
                # and 'pk' not in view.kwargs:
                return True
        else:
            # method is 'GET' mainly, one needs to be contributor to read it
            if project_members.filter(user=request.user).exists():
                return True
        return False
