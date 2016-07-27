from django.db import models


class PartnerEmployee(models.Model):

    def get_data_from_server(self):
        return "PartnerEmployee"

class Search(models.Model):
    key = models.CharField(max_length=200)

    def __str__(self):
        return self.key