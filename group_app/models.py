import re
from django.db import models
from login_app.models import Registration

class GroupManager(models.Manager):
    def basic_validator(self, post_data):
        errors ={}
        org_name_check = self.filter(org_name=post_data['org_name'])
        if org_name_check:
            errors['org_name'] = "Organization already in use" 
        if len(post_data['org_name']) == 0:
            errors['org_name'] = "Please provide Orginization Name"
        if len(post_data['org_name']) < 5:
            errors['org_name'] = "Organization Name should be 5 or more characters"
        if len(post_data['description']) < 10:
            errors['description'] = "Description should be 10 or more characters"
        return errors


class Group(models.Model):
    publisher = models.ForeignKey(Registration, related_name="groups", on_delete =models.CASCADE)
    org_name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    join = models.ManyToManyField(Registration, related_name="joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GroupManager()
