# accounts / schema.py
import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model, authenticate
from graphene_django.types import DjangoObjectType
from graphql_jwt.shortcuts import get_token, create_refresh_token
from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import get_payload, jwt_decode, get_user_by_payload
from datetime import timedelta
from graphene.types.generic import GenericScalar
from graphene_file_upload.scalars import Upload  # Import Upload scalar

# ===================== User Types =====================
User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # Exclude password field for security
        exclude = ('password',)


# ===================== Custom Obtain Token =====================
class CustomObtainJSONWebToken(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    refresh_token = graphene.String()
    payload = graphene.Field(GenericScalar)

    @classmethod
    def mutate(cls, root, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception("Incorrect username or password")

        if not user.is_active:
            raise Exception("User account is inactive")

        token = get_token(user)
        refresh_token = create_refresh_token(user)
        payload = get_payload(token, info.context)

        return cls(token=token, refresh_token=refresh_token, payload=payload)


# ===================== Refresh Access Token =====================
class RefreshAccessToken(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String(required=True)

    token = graphene.String()
    payload = graphene.Field(GenericScalar)
    refresh_token = graphene.String()

    @staticmethod
    def mutate(root, info, refresh_token):
        try:
            payload = jwt_decode(refresh_token)
            user = get_user_by_payload(payload)
            if not user or not user.is_active:
                raise Exception("Invalid or inactive user")

            # Verify refresh token is still valid (optional, depends on your logic)
            # graphql_jwt.refresh_token.utils.check_refresh_token(refresh_token)

            token = get_token(user)
            new_refresh_token = create_refresh_token(user)
            return RefreshAccessToken(token=token, refresh_token=new_refresh_token, payload=payload)
        except Exception as e:
            raise Exception(f"Error refreshing token: {e}")


# ===================== Input Types =====================
class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UpdateUserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    gender = graphene.String()
    position = graphene.String()
    department = graphene.String()
    # Change profile_picture to Upload type
    profile_picture = Upload(required=False)
    password = graphene.String()  # For password change


# ===================== CREATE User =====================
class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    @staticmethod
    def mutate(root, info, input):
        User = get_user_model()
        if User.objects.filter(username=input.username).exists():
            raise Exception("Username already exists")
        if User.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")

        user = User.objects.create_user(
            username=input.username,
            email=input.email,
            password=input.password
        )

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, ok=True, token=token, refresh_token=refresh_token)


# ===================== UPDATE User =====================
class UpdateUser(graphene.Mutation):
    class Arguments:
        # No ID needed, user is identified from context (login_required)
        input = UpdateUserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        # Iterate through input fields and update user instance
        for field, value in input.items():
            if value is not None:
                if field == "password":
                    # Handle password change securely
                    if value:  # Only change if a new password is provided
                        user.set_password(value)
                elif field == "profile_picture":
                    # Handle file upload
                    user.profile_picture = value
                else:
                    setattr(user, field, value)

        user.save()
        return UpdateUser(ok=True, user=user)


# ===================== Queries =====================
class AccountsQuery(graphene.ObjectType):
    # Get user by ID (e.g., for admin purposes, ensure proper permissions)
    user = graphene.Field(UserType, id=graphene.ID())
    # Get the currently logged-in user's details
    whoami = graphene.Field(UserType)

    # @login_required # Consider if this needs login
    def resolve_user(parent, info, id):
        # Add permission checks if needed
        try:
            return get_user_model().objects.get(id=id)
        except get_user_model().DoesNotExist:
            return None

    @login_required
    def resolve_whoami(self, info):
        user = info.context.user
        # Redundant check due to @login_required, but good practice
        if user.is_anonymous:
            raise Exception("Authentication Failure: You must be signed in")
        return user


# ===================== Mutations =====================
class AccountsMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    # delete_user = DeleteUser.Field() # Add if needed

    # Authentication mutations
    token_auth = CustomObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    refresh_access_token = RefreshAccessToken.Field()
    # revoke_token = graphql_jwt.Revoke.Field() # Add if needed

# # accounts / schema.py
# import graphene
# import graphql_jwt
# # from graphene_django.types import DjangoObjectType, ObjectType
# # from django.contrib.auth.models import User
# from graphql_jwt.decorators import login_required
# # ----------------------------------------------------------------
# from django.contrib.auth import get_user_model
# from graphene_django.types import DjangoObjectType
# from graphql_jwt.shortcuts import get_token, create_refresh_token
# from graphql_jwt.settings import jwt_settings
# from graphql_jwt.utils import get_payload, jwt_decode, get_user_by_payload
# from datetime import timedelta
# from django.contrib.auth import authenticate
# from graphene.types.generic import GenericScalar
#
# # ----------------------------------------------------------------
#
# # ===================== User Types =====================
# User = get_user_model()
#
#
# class UserType(DjangoObjectType):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# # ----------------------------------------------------------------
# # class CustomObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
# #     refresh_token = graphene.String()
# #
# #     # class Arguments:
# #     #     refresh_token = graphene.String()
# #     @classmethod
# #     def resolve(cls, root, info, **kwargs):
# #         result = super().resolve(root, info, **kwargs)
# #         user = info.context.user
# #         # refresh_token = jwt_settings.JWT_REFRESH_TOKEN_HANDLER(user, info.context)
# #         refresh_token = create_refresh_token(user)
# #         # refresh_expires_in = int(jwt_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds())
# #         # return {
# #         #     'token': result.token,
# #         #     'payload': result.payload,
# #         #     # 'refresh_expires_in': refresh_expires_in,
# #         #     'refresh_token': refresh_token
# #         # }
# #         return cls(
# #             token=result.token,
# #             payload=result.payload,
# #             refresh_token=refresh_token
# #         )
# # ----------------------------------------------------------------
#
# class CustomObtainJSONWebToken(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#
#     token = graphene.String()
#     refresh_token = graphene.String()
#     # payload = graphene.Field(graphene.JSONString)
#     payload = graphene.Field(GenericScalar)
#
#     @classmethod
#     def mutate(cls, root, info, username, password):
#         # اعتبارسنجی کاربر
#         user = authenticate(username=username, password=password)
#         if user is None:
#             raise Exception("نام کاربری یا رمز عبور اشتباه است")
#
#         if not user.is_active:
#             raise Exception("حساب کاربری غیرفعال است")
#
#         token = get_token(user)
#         refresh_token = create_refresh_token(user)
#         payload = get_payload(token, info.context)
#
#         return cls(token=token, refresh_token=refresh_token, payload=payload)
#
#
# # ----------------------------------------------------------------
# class RefreshAccessToken(graphene.Mutation):
#     class Arguments:
#         refresh_token = graphene.String(required=True)
#
#     token = graphene.String()
#     # payload = graphene.Field(graphene.JSONString)
#     payload = graphene.Field(GenericScalar)
#     refresh_token = graphene.String()
#
#     @staticmethod
#     def mutate(root, info, refresh_token):
#         # decode the refresh token
#         # payload = graphql_jwt.utils.jwt_decode(refresh_token)
#         # user = graphql_jwt.utils.get_user_by_payload(payload)
#         payload = jwt_decode(refresh_token)
#         user = get_user_by_payload(payload)
#         if not user or not user.is_active:
#             raise Exception("Invalid or inactive user")
#
#         # token = graphql_jwt.shortcuts.get_token(user)
#         token = get_token(user)
#
#         refresh_token = create_refresh_token(user)
#         return RefreshAccessToken(token=token, refresh_token=refresh_token, payload=payload)
#
#         # return RefreshAccessToken(token=token, payload=payload)
#
#
# # ===================== Input Types =====================
#
#
# class UserInput(graphene.InputObjectType):
#     username = graphene.String()
#     email = graphene.String()
#     password = graphene.String()
#     # is_active = graphene.Boolean()
#     # is_staff = graphene.Boolean()
#     # is_superuser = graphene.Boolean()
#
#
# # ----------------------------------------------------------------
# class UpdateUserInput(graphene.InputObjectType):
#     first_name = graphene.String()
#     last_name = graphene.String()
#     email = graphene.String()
#     gender = graphene.String()
#     position = graphene.String()
#     department = graphene.String()
#     profile_picture = graphene.String()
#     password = graphene.String()
#
#
# # ===================== CREATE =====================
# # class CreateUser(graphene.Mutation):
# #     class Arguments:
# #         input = UserInput(required=True)
# #
# #     ok = graphene.Boolean(default_value=False)
# #     user = graphene.Field(UserType)
# #
# #     @staticmethod
# #     def mutate(parent, info, input=None):
# #         user_instance = User.objects.create_user(input.username, input.email, input.password)
# #         ok = True
# #         return CreateUser(user=user_instance, ok=ok)
#
# class CreateUser(graphene.Mutation):
#     class Arguments:
#         input = UserInput(required=True)
#
#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)
#     token = graphene.String()
#     refresh_token = graphene.String()
#
#     @staticmethod
#     def mutate(root, info, input):
#         User = get_user_model()
#         if User.objects.filter(username=input.username).exists():
#             raise Exception("Username already exists")
#
#         user = User.objects.create_user(
#             username=input.username,
#             email=input.email,
#             password=input.password
#         )
#
#         token = get_token(user)
#         refresh_token = create_refresh_token(user)
#
#         return CreateUser(user=user, ok=True, token=token, refresh_token=refresh_token)
#
#
# # ===================== UPDATE =====================
#
#
# class UpdateUser(graphene.Mutation):
#     class Arguments:
#         input = UpdateUserInput(required=True)
#
#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)
#
#     @login_required
#     def mutate(self, info, input):
#         user = info.context.user
#         # for field, value in input.items():
#         #     if value is not None:
#         #         setattr(user, field, value)
#
#         for field, value in input.items():
#             if value is not None:
#                 if field == "password":
#                     user.set_password(value)
#                 else:
#                     setattr(user, field, value)
#         user.save()
#         return UpdateUser(ok=True, user=user)
#
#
# # ===================== Queries =====================
#
# class AccountsQuery(graphene.ObjectType):
#     user = graphene.Field(UserType, id=graphene.ID())
#     whoami = graphene.Field(UserType)
#
#     @login_required
#     def resolve_user(parent, info, id=None):
#         if id:
#             return get_user_model().objects.get(id=id)
#         return None
#
#     def resolve_whoami(self, info):
#         user = info.context.user
#         if user.is_anonymous:
#             raise Exception("Authentication Failure: You must be signed in")
#         return user
#
#
# # class AccountsQuery(ObjectType):
# #     user = graphene.Field(UserType, id=graphene.ID())
# #
# #     @login_required
# #     def resolve_user(parent, info, **kwargs):
# #         # user = info.context.user
# #         # # if not user.is_authenticated:
# #         # if user.is_anonymous:
# #         #     raise Exception('Not authenticated! YOU ARE NOT LOGGED IN')
# #         id = kwargs.get('id')
# #         if id is not None:
# #             return User.objects.get(id=id)
# #         return None
#
# # ===================== Mutations =====================
# class AccountsMutation(graphene.ObjectType):
#     create_user = CreateUser.Field()
#     update_user = UpdateUser.Field()
#     # delete_user = DeleteUser.Field()
#     # token_auth = graphql_jwt.ObtainJSONWebToken.Field()  # FOR THE FIRST TIME WE CREATE TOKEN
#     verify_token = graphql_jwt.Verify.Field()  # TO VERIFY USERS TOKEN
#     refresh_token = graphql_jwt.Refresh.Field()
#     # TO GIVE NEW TOKEN TO A USER THAT ALREADY HAS TOKEN AND WANTS TO REFTESH IT
#     refresh_access_token = RefreshAccessToken.Field()
#     token_auth = CustomObtainJSONWebToken.Field()
#
# # -------------------------------------------------------------------------------------------------------------------
