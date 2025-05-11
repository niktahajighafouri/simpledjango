# tasks/schema.py
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required  # Assuming you use graphql_jwt for auth
from django.contrib.auth.models import Group  # To check user groups
from django.conf import settings  # To get AUTH_USER_MODEL
from .models import Task, SubTask  # Your task models

# Get the User model dynamically
User = settings.AUTH_USER_MODEL


# Helper function to check if a user is in a specific group
def is_user_in_group(user, group_name):
    if user.is_anonymous:
        return False
    return user.groups.filter(name=group_name).exists()


# GraphQL Types for your models
class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"


class SubTaskType(DjangoObjectType):
    class Meta:
        model = SubTask
        fields = "__all__"


# Input types for mutations
class TaskInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    due_date = graphene.Date(required=True)
    status = graphene.String(default_value='TODO')  # Default to 'To Do'
    priority = graphene.String(default_value='MEDIUM')  # Default to 'Medium'
    assigned_to_id = graphene.ID(required=False)  # User ID to assign the task


class SubTaskInput(graphene.InputObjectType):
    task_id = graphene.ID(required=True)  # ID of the parent Task
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    status = graphene.String(default_value='TODO')


class UpdateTaskInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    due_date = graphene.Date()
    status = graphene.String()
    priority = graphene.String()
    assigned_to_id = graphene.ID()


class UpdateSubTaskInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    status = graphene.String()


# Mutations for Tasks
class CreateTaskMutation(graphene.Mutation):
    class Arguments:
        input = TaskInput(required=True)

    task = graphene.Field(TaskType)
    ok = graphene.Boolean()

    @login_required
    def mutate(root, info, input):
        if not is_user_in_group(info.context.user, 'Managers'):
            raise Exception('Permission Denied: Only Managers can create tasks.')

        assignee = None
        if input.assigned_to_id:
            try:
                assignee = User.objects.get(pk=input.assigned_to_id)
            except User.DoesNotExist:
                raise Exception('Assigned user not found.')

        task_instance = Task(
            title=input.title,
            description=input.description,
            due_date=input.due_date,
            status=input.status,
            priority=input.priority,
            created_by=info.context.user,
            assigned_to=assignee
        )
        task_instance.save()
        return CreateTaskMutation(task=task_instance, ok=True)


class UpdateTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateTaskInput(required=True)

    task = graphene.Field(TaskType)
    ok = graphene.Boolean()

    @login_required
    def mutate(root, info, id, input):
        try:
            task_instance = Task.objects.get(pk=id)
        except Task.DoesNotExist:
            raise Exception('Task not found.')

        user = info.context.user
        is_manager = is_user_in_group(user, 'Managers')
        is_creator = task_instance.created_by == user
        is_assignee = task_instance.assigned_to == user

        if not (is_manager or is_creator or is_assignee):
            raise Exception('Permission Denied: You cannot modify this task.')

        # Managers can update all fields
        # Creators/Assignees can only update status and description (example logic)
        if input.title and is_manager: task_instance.title = input.title
        if input.description: task_instance.description = input.description  # Allow assignee/creator to add notes
        if input.due_date and is_manager: task_instance.due_date = input.due_date
        if input.status: task_instance.status = input.status
        if input.priority and is_manager: task_instance.priority = input.priority
        if input.assigned_to_id and is_manager:
            try:
                assignee = User.objects.get(pk=input.assigned_to_id)
                task_instance.assigned_to = assignee
            except User.DoesNotExist:
                raise Exception('Assigned user not found.')

        task_instance.save()
        return UpdateTaskMutation(task=task_instance, ok=True)


class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(root, info, id):
        if not is_user_in_group(info.context.user, 'Managers'):
            raise Exception('Permission Denied: Only Managers can delete tasks.')
        try:
            task_instance = Task.objects.get(pk=id)
            task_instance.delete()
            return DeleteTaskMutation(ok=True, message='Task deleted successfully')
        except Task.DoesNotExist:
            raise Exception('Task not found.')


# Mutations for SubTasks
class CreateSubTaskMutation(graphene.Mutation):
    class Arguments:
        input = SubTaskInput(required=True)

    sub_task = graphene.Field(SubTaskType)
    ok = graphene.Boolean()

    @login_required
    def mutate(root, info, input):
        try:
            parent_task = Task.objects.get(pk=input.task_id)
        except Task.DoesNotExist:
            raise Exception('Parent Task not found.')

        user = info.context.user
        # Allow creation if user is manager, creator of parent task, or assigned to parent task
        is_manager = is_user_in_group(user, 'Managers')
        is_creator_of_parent = parent_task.created_by == user
        is_assignee_of_parent = parent_task.assigned_to == user

        if not (is_manager or is_creator_of_parent or is_assignee_of_parent):
            raise Exception('Permission Denied: You cannot add subtasks to this task.')

        sub_task_instance = SubTask(
            task=parent_task,
            title=input.title,
            description=input.description,
            status=input.status
        )
        sub_task_instance.save()
        return CreateSubTaskMutation(sub_task=sub_task_instance, ok=True)


class UpdateSubTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateSubTaskInput(required=True)

    sub_task = graphene.Field(SubTaskType)
    ok = graphene.Boolean()

    @login_required
    def mutate(root, info, id, input):
        try:
            sub_task_instance = SubTask.objects.get(pk=id)
        except SubTask.DoesNotExist:
            raise Exception('SubTask not found.')

        user = info.context.user
        parent_task = sub_task_instance.task

        is_manager = is_user_in_group(user, 'Managers')
        is_creator_of_parent = parent_task.created_by == user
        is_assignee_of_parent = parent_task.assigned_to == user

        if not (is_manager or is_creator_of_parent or is_assignee_of_parent):
            raise Exception('Permission Denied: You cannot modify this subtask.')

        if input.title: sub_task_instance.title = input.title
        if input.description: sub_task_instance.description = input.description
        if input.status: sub_task_instance.status = input.status

        sub_task_instance.save()
        return UpdateSubTaskMutation(sub_task=sub_task_instance, ok=True)


class DeleteSubTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(root, info, id):
        try:
            sub_task_instance = SubTask.objects.get(pk=id)
        except SubTask.DoesNotExist:
            raise Exception('SubTask not found.')

        user = info.context.user
        parent_task = sub_task_instance.task

        is_manager = is_user_in_group(user, 'Managers')
        is_creator_of_parent = parent_task.created_by == user
        is_assignee_of_parent = parent_task.assigned_to == user

        if not (is_manager or is_creator_of_parent or is_assignee_of_parent):
            raise Exception('Permission Denied: You cannot delete this subtask.')

        sub_task_instance.delete()
        return DeleteSubTaskMutation(ok=True, message='SubTask deleted successfully')


class TasksQuery(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)
    my_tasks = graphene.List(TaskType)  # Tasks assigned to the logged-in user
    task_by_id = graphene.Field(TaskType, id=graphene.ID(required=True))
    subtasks_for_task = graphene.List(SubTaskType, task_id=graphene.ID(required=True))

    @login_required
    def resolve_all_tasks(root, info):
        user = info.context.user
        if is_user_in_group(user, 'Managers'):
            return Task.objects.all().order_by('-created_at')
        # Regular users only see tasks assigned to them or created by them
        return Task.objects.filter(models.Q(assigned_to=user) | models.Q(created_by=user)).distinct().order_by(
            '-created_at')

    @login_required
    def resolve_my_tasks(root, info):
        user = info.context.user
        return Task.objects.filter(assigned_to=user).order_by('due_date')

    @login_required
    def resolve_task_by_id(root, info, id):
        try:
            task = Task.objects.get(pk=id)
        except Task.DoesNotExist:
            return None

        user = info.context.user
        is_manager = is_user_in_group(user, 'Managers')
        is_assigned_user = task.assigned_to == user
        is_creator = task.created_by == user

        if is_manager or is_assigned_user or is_creator:
            return task
        return None  # Or raise an exception for unauthorized access

    @login_required
    def resolve_subtasks_for_task(root, info, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return []

        user = info.context.user
        is_manager = is_user_in_group(user, 'Managers')
        is_assigned_to_parent_task = task.assigned_to == user
        is_creator_of_parent_task = task.created_by == user

        if is_manager or is_assigned_to_parent_task or is_creator_of_parent_task:
            return SubTask.objects.filter(task=task).order_by('created_at')
        return []  # Or raise an exception


class TasksMutation(graphene.ObjectType):
    create_task = CreateTaskMutation.Field()
    update_task = UpdateTaskMutation.Field()
    delete_task = DeleteTaskMutation.Field()
    create_sub_task = CreateSubTaskMutation.Field()
    update_sub_task = UpdateSubTaskMutation.Field()
    delete_sub_task = DeleteSubTaskMutation.Field()
