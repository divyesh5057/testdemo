from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, password2=None,**kwargs):
        print("*********",kwargs)
        """
        Creates and saves a User with the given email, name and password.
        """
        
        if not email:
            raise ValueError('Users must have an email address')
        if 'is_admin' in kwargs:
            admin_status=kwargs['is_admin']
        else:
            admin_status=False
        
        if 'phone_number' in kwargs:
            phone_number=kwargs['phone_number']
        else:
            phone_number=None
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin=admin_status,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# /home/koli/Documents/banner_project/banners_01/ba nners/banner_apis/mediafiles/bannerimages/Screenshot_from_2023-01-19_12-28-06.png
#custome user
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=200,)
    full_name=models.CharField(max_length=60,null=True,blank=True)
    profilei_image = models.ImageField(upload_to='profileimages/', blank=True, null=True)
    designation=models.CharField(max_length=20,null=True,blank=True)
    date_of_birth=models.DateTimeField(null=True,blank=True)
    date_of_joining=models.DateTimeField(null=True,blank=True)
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    website=models.CharField(max_length=40,null=True,blank=True)
    gender=models.CharField(max_length=10,null=True,blank=True)
    otp = models.CharField(max_length = 9, blank = True, null= True)
    count = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Category_db(models.Model):
    name = models.CharField(unique=True,max_length=50,null=True,blank=True) 
    
    def __str__(self):
     return str(self.id)

class banner_db(models.Model):
    category = models.ForeignKey(Category_db,on_delete=models.CASCADE)
    banner_img = models.ImageField(upload_to='bannerimages/', blank=True, null=True)
    banner_url = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return f"{self.banner_img} ({self.category.name})"

class AdminBanners(models.Model):
    banner_images=models.ImageField(upload_to='admin_banners/')