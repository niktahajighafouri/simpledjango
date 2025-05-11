# simpledjango / schema.py

import graphene_django
import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from rest_framework.authtoken.views import obtain_auth_token
import home.schema
import accounts.schema
import tasks.schema


# from django.contrib.auth.models import User
# from graphql_jwt.decorators import login_required


class Query(tasks.schema.TasksQuery,home.schema.HomeQuery, accounts.schema.AccountsQuery, graphene.ObjectType):
    pass


class Mutation(tasks.schema.TasksMutation,home.schema.HomeMutation, accounts.schema.AccountsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

# ------------------------

# mutation createPerson {
#     createPerson(input: {
#         name: "nikita"
#         age: 24
#     }){person{name, age}}
# }


# {
#     "data": {
#         "createPerson": {
#             "person": {
#                 "name": "nikita",
#                 "age": "24"
#             }
#         }
#     }
# }

# ------------------------

# query GetAllPersons {
#     persons {
#         name
#         id
#         age
#     }
# }

# {
#   "data": {
#     "persons": [
#       {
#         "name": "yasna",
#         "id": "1",
#         "age": "21"
#       },
#       {
#         "name": "taha",
#         "id": "2",
#         "age": "33"
#       },
#       {
#         "name": "mohammad",
#         "id": "3",
#         "age": "14"
#       },
#       {
#         "name": "nikita",
#         "id": "4",
#         "age": "24"
#       },
#       {
#         "name": "nikita",
#         "id": "5",
#         "age": "24"
#       },
#       {
#         "name": "bob",
#         "id": "6",
#         "age": "24"
#       },
#       {
#         "name": "bob",
#         "id": "7",
#         "age": "24"
#       },
#       {
#         "name": "bob",
#         "id": "8",
#         "age": "24"
#       },
#       {
#         "name": "samim",
#         "id": "9",
#         "age": "24"
#       },
#       {
#         "name": "roshanak",
#         "id": "10",
#         "age": "24"
#       },
#       {
#         "name": "rosha",
#         "id": "11",
#         "age": "24"
#       }
#     ]
#   }
# }


# ------------------------

# mutation updatePerson {
#   updatePerson(id: 10, input: {name: "roshaanak"}) {
#     ok
#     person {
#       name
#       age
#       id
#     }
#   }


# {
#   "data": {
#     "updatePerson": {
#       "ok": true,
#       "person": {
#         "name": "roshaanak",
#         "age": "24",
#         "id": "10"
#       }
#     }
#   }
# }
# ------------------------
