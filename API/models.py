from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import re

class Librarian(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Member(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=200, null=True)
    nic = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=500, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        # Validate NIC and extract birthday and gender
        if self.nic:
            self.birthday, self.gender = self.extract_birthday_and_gender_from_nic()

    def extract_birthday_and_gender_from_nic(self):
        """
        Extract birthday and gender from Sri Lankan NIC number.
        Old NIC format: 9 digits followed by a letter (e.g., 900000000V)
        New NIC format: 12 digits (e.g., 200000000000)
        """
        if len(self.nic) == 10:
            year = int(self.nic[:2])
            day_of_year = int(self.nic[2:5])
        elif len(self.nic) == 12:
            year = int(self.nic[:4])
            day_of_year = int(self.nic[4:7])
        else:
            raise ValueError("Invalid NIC format")

        # Determine the correct year
        if len(self.nic) == 10:
            if year > 50:
                year += 1900
            else:
                year += 2000

        # Determine the gender
        if day_of_year > 500:
            day_of_year -= 500
            gender = 'Female'
        else:
            gender = 'Male'

        # Calculate the birth date
        birthday = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
        return birthday.date(), gender

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    number_of_books = models.IntegerField(default=1)

class IssuedBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issued_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issued_books')
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=True)

    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            # Assuming a simple fine calculation: LKR 50 per day late
            days_late = (self.return_date - self.due_date).days
            self.fine = days_late * 50
        else:
            self.fine = 0

    def save(self, *args, **kwargs):
        self.calculate_fine()
        super().save(*args, **kwargs)
