from django.db import models


class TotalArchive(models.Model):
    total_products = models.IntegerField()
    total_users = models.IntegerField()
    total_categories = models.IntegerField()

    class Meta:
        db_table = "total_archive"
