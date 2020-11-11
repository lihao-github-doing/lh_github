from django.db import models

# Create your models here.

# 文章表
class TArticle(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    cate = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 't_article'

# 分类表
class TCategory(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_category'



