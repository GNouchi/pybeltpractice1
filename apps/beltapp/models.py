from django.db import models
from django.core.validators import validate_email 
import datetime
import bcrypt

#  add models
class UserManager(models.Manager):
    def regValidator(self, postData):
        result = {'errors':[]}
        if len(postData['first_name']) <1:
            result['errors'].append("First Name too short")
        if len(postData['last_name']) <1:
            result['errors'].append("Last Name too short")
        if len(postData['email']) <1:
            result['errors'].append("Email too short")
        if len(postData['password']) <8:
            result['errors'].append("Password too short")
        if postData['password'] !=postData['confirm_password']:
            result['errors'].append("Passwords do not match")
        try:
            if postData['last_name'].isalpha() ==False or postData['first_name'].isalpha() ==False:
                result['errors'].append("Name fields can only be english letters")
        except:
            pass
        try:
            validate_email(postData['email'])
        except:
            result['errors'].append("Invalid email")
        throwaway = User.objects.filter(email = postData['email'])
        if len(throwaway)> 0:
            result['errors'].append("Please use another email")
        if len(result['errors'])> 0:
            print("errors found, escaping now...")
            return result
# ******************************** VALIDATION PASS *************************************
        print("regValidator Pass")
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        hash1= hash1.decode()        
        newUser = User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hash1,
        )
        result['user_id'] = newUser.id
        return result

    def loginValidator(self, postData):
        result = {'errors':[]}
        throwaway = User.objects.filter(email = postData['email'])
        if len(throwaway) > 0:
            if bcrypt.checkpw(postData['password'].encode(),throwaway[0].password.encode() ):
                result['user_id'] = throwaway[0].id
                return result
        result['errors'].append("Password or Email did not match")
        return result

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_d = models.DateTimeField(auto_now_add = True)
    update_d = models.DateTimeField(auto_now = True)
    objects = UserManager()


# ----------------------------------------------------------------------------------
class TripManager(models.Manager):
    def tripValidator(self, postData):
        result = {'errors':[]}
        today = datetime.datetime.today().date()
        if len(postData['destination']) <1:
            result['errors'].append("Please include a Destination")
        if len(postData['description']) <1:
            result['errors'].append("Please include a Description")
        if len(postData['trip_start']) <1:
            result['errors'].append("Please include a Start Date")
        else: 
            start = datetime.datetime.strptime(postData['trip_start'], "%Y-%m-%d").date()
            if start < today:
                result['errors'].append("Start Date must be a future date")
        if len(postData['trip_end']) <1:
            result['errors'].append("Please include an End Date")
        else:
            end = datetime.datetime.strptime(postData['trip_end'], "%Y-%m-%d").date()
            if end < today:
                result['errors'].append("End Date must be a future date")
            if len(postData['trip_start']) >1:
                if end < start:
                    result['errors'].append("End date must be after start date")            
        throwaway = User.objects.filter(id = postData['user_id'])
        if len(throwaway) == 0:
            result['errors'].append("user not found")
        if len(result['errors']) > 0:
            print("errors found, escaping now...")
            return result
# ******************************** VALIDATION PASS *************************************
        print("Trip create pass")
        newTrip = Trip.objects.create(
            owner = throwaway[0],
            destination = postData['destination'],
            description = postData['description'],
            trip_start = postData['trip_start'],
            trip_end = postData['trip_end'],
        )
        result['newTrip'] = newTrip
        return result
        

class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    attendees = models.ManyToManyField(User, related_name= "trips")
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    trip_start = models.DateTimeField(auto_now = False)
    trip_end = models.DateTimeField(auto_now = False)
    update_d = models.DateTimeField(auto_now = True)
    objects = TripManager()
    