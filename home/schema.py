# home/schema
import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Person, Car

# import graphql_jwt
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.views import obtain_auth_token
# from django.contrib.auth.models import User
# from graphql_jwt.decorators import login_required

# --------------------------------------------------------------------------------------------------
# to show all data to user


class CarType(DjangoObjectType):
    class Meta:
        model = Car


class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        # if you do not add fields it means all of them !!!

# to show some data to user

# query


class HomeQuery(ObjectType):
    persons = graphene.List(PersonType)
    cars = graphene.List(CarType)

    def resolve_persons(parent, info, **kwargs):
        # تمام اطلاعات داخل مدل پرسن رو داری ریترن میکنی
        return Person.objects.all()

    def resolve_cars(parent, info, **kwargs):
        return Car.objects.all()


class PersonInput(graphene.InputObjectType):
    name = graphene.String()
    age = graphene.Int()


class CarInput(graphene.InputObjectType):
    name = graphene.String()
    year = graphene.Int()
    # beaouse we get and use the persons id and it should be int beacouse of the foreign key
    # person_id = graphene.Int()     # when we have many to many field we have to send a list
    # we are giving a list of ids or a list of ints to person id
    people_id = graphene.List(graphene.ID)
    # you have to write graphene.ID with no ()


class CreateCar(graphene.Mutation):
    class Arguments:
        input = CarInput()
    car = graphene.Field(CarType)
    ok = graphene.Boolean(default_value=False)

# """  when we have many to many field we have to write set   """
    @staticmethod
    def mutate(parent, info, input=None):
        people_list = []
        for person_id in input.people_id:
            person_instance = Person.objects.get(id=person_id)
            people_list.append(person_instance)

        car_instance = Car.objects.create(name=input.name, year=input.year)
        # you cant give people here : beacous it is many to many field in models
        car_instance.person.set(people_list)
        ok = True
        return CreateCar(car=car_instance, ok=ok)


# """  when we set one car to one person  """
    # @staticmethod
    # # we type none for info so that if it wont come we don't get errors
    # def mutate(parent, info, input=None):
    #     person_instance = Person.objects.get(
    #         id=input.person_id)  # we expect to get persons id
    #     # person_instance =Person.objects.get(id=input.id)
    #     car_instance = Car.objects.create(
    #         name=input.name, year=input.year, person=person_instance)
    #     ok = True
    #     return CreateCar(car=car_instance, ok=ok)


class CreatePerson(graphene.Mutation):

    """    if you  are going to use the arguments and fields in other places , you would have to define them every time  instead we will create Input classes!    """
    # class Arguments:
    #     name = graphene.String()
    #     age = graphene.Int()

    class Arguments:
        """  because i want all the arguments to be required i change the require for person input  """
        input = PersonInput(required=True)
    # to pass person to mutate method:
    person = graphene.Field(PersonType)

    ok = graphene.Boolean(default_value=False)

    @staticmethod
    def mutate(parent, info, input=None):
        # create bellow calls save by its self!
        person_instance = Person.objects.create(name=input.name, age=input.age)
        # person_instance.save()
        ok = True
        # to show the user that ther has been a person created!
        return CreatePerson(person=person_instance, ok=ok)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID()    # the only differance with int is : it ensures that it is unic !
        # id = graphene.Int()
    ok = graphene.Boolean(default_value=False)
    person = graphene.Field(PersonType)

    @staticmethod
    def mutate(parent, info, id):
        person_instance = Person.objects.get(id=id)
        person_instance.delete()
        ok = True
        return DeletePerson(person=person_instance, ok=ok)


class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PersonInput()

    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    # writing @static method wont make any change:
    def mutate(parent, info, id, input=None):
        person_instance = Person.objects.get(id=id)
        person_instance.name = input.name if input.name is not None else person_instance.name
        person_instance.age = input.age if input.age is not None else person_instance.age
        person_instance.save()
        ok = True
        return UpdatePerson(person=person_instance, ok=ok)


# mutate
class HomeMutation(graphene.ObjectType):
    # WE PASS ALL THE MUTATES AS FEILDS
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()
    create_car = CreateCar.Field()
    # we usually get only id field for delete and we wont use PersonInput

