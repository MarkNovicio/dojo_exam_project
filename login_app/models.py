import re

from django.db import models
#from datetime import datetime
import bcrypt

class RegistrationManager(models.Manager):
    def basic_validator(self, post_data):
        errors={}
       # today = datetime.today()
        email_check = self.filter(email=post_data['email'])
        if email_check:
            errors['email'] = "Email already in use" 
            #compares user email input to what is in database

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 characters"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must contain 8 characters"
        if len(post_data['password']) < 0:
            errors['password'] = "Password must contain 8 characters"
        if post_data['confirm_pw'] != post_data['password']:
            errors['confirm_pw'] = "Confirm Password must match Password"
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0] 
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def edit_validator(self, post_data, user):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if post_data['first_name'] != '':
            if (len(post_data['first_name']) < 2 or len(post_data['first_name']) > 50):
                errors['first_name'] = "First name must be between 2 - 50 characters long"
        
        if not bcrypt.checkpw(post_data['current_password'].encode(), user.password.encode()):
            errors['password']=  "Password does not match, cannot edit profile"
            
        if post_data['last_name'] != '':
            if len(post_data['last_name']) < 2:
                errors['last_name'] = "Last name must have at least 2 characters"

        if post_data['email'] != user.email:
            try:
                Registration.objects.get(email =post_data['email'])
                errors['email'] = "Email exists already"
            except:
                pass
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        
        return errors

class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    objects = RegistrationManager()

    def __repr__(self):
        return f'Name: {self.first_name} {self.last_name}|email: {self.email} | password: {self.password}'


