from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class PlaceOfInstallation(models.Model):
    district_name = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    district_code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.city_name}, {self.district_name}"

class SolarPanel(models.Model):
    capacity = models.FloatField()
    inclination = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(90)])

    # null=True and blank=True when a property may not be filled or known
    efficiency = models.FloatField(null=True, blank=True)
    panel_type = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    model_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.capacity} kW, {self.inclination} degrees"

class Customer(models.Model):
    user = models.OneToOneField('MyUser', on_delete=models.CASCADE)
    place_of_installation = models.ForeignKey(PlaceOfInstallation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class EnergyGeneration(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    solar_panel = models.ForeignKey(SolarPanel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    solar_irradiance = models.FloatField()

    def calculate_energy_generation(self):
        # Calculate energy generation using solar irradiance and panel capacity
        return self.solar_panel.capacity * self.solar_irradiance

    def __str__(self):
        return f"{self.solar_panel} - {self.customer} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The Email field must be set.')
        if not username:
            raise ValueError('The Username field must be set.')

        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # responsible for querying the database and returning instances of the model
    objects = MyUserManager()

    def __str__(self):
        return self.email
