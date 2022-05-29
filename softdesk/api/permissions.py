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
        print('rights checked against view:', view)

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # here the request.user.is_authenticated
        print('permissions checked against object:', obj)
        # hence check if request.user is contributor
        print('check if contributor')
        if obj.pk:
            current_obj_id = obj.pk
            if isinstance(obj, Project):
                project_id = current_obj_id
                level = 'Project'
                print("project id", level, project_id)
            if isinstance(obj, Issue):
                project_id = Issue.objects.get(pk=current_obj_id).project
                print("prj id", level, project_id)
                level = 'Issue'
            if isinstance(obj, Comment):
                project_id = Comment.objects.select_related(issue).get(pk=current_obj_id)
                level = 'Comment'
                print("prj id", level, project_id)
            project_members = Contributor.objects.filter(project=project_id)
            print('Members', project_members)

        # let superuser be superuser == have full access
        if request.user.is_superuser:
            return bool(request.user and request.user.is_superuser)
        # only the owner of one object is permitted ti Update or Delete it
        if request.method in self.edit_delete_methods:
            print("edit_delete_methods for: ", request.method, 'author: ', request.user)
            return obj.author_user == request.user
        elif request.method in self.create_methods:
            print("create_methods for: ", request.method, 'author: ', request.user)
            # authenticated user is allowed to create a new project
            if isinstance(obj, Project):
                print("action: ", request.method, " Project: ", obj, 'author: ', request.user)
                # and 'pk' not in view.kwargs:
                return True
            else:
                # Contributor is allowed to create Issues or Comments
                # check if the autor_user is contributor
                print("action: ", request.method, " not Project: ", obj, 'author: ', request.user)
        else:
            # method is 'GET' mainly, one needs to be contributor to read it
            print("action: ", request.method, " obj: ", obj.pk, 'author: ', request.user)
            if project_members.filter(user=request.user).exists():
                print('contributor')
                return True
# @now
        return False