from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# sign in data : username , email , phone_number , password

# signup requirements : email , password


class Car(models.Model):
    # person = models.ForeignKey(Person, on_delete=models.CASCADE)
    person = models.ManyToManyField(Person)
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name


# -----------------------------

# mutation{
#   createCar(input:{name:"audi",personId:11,year:2011}){
#     ok
#     car{
#       name
#       year
#       person{
#         name
#       }
#     }
#   }
# }
