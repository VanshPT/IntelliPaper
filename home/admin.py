from django.contrib import admin
from .models import ResearchPaper, Folder, Readlist, Notes,Citation
# Register your models here.
admin.site.register(ResearchPaper)
admin.site.register(Folder)
admin.site.register(Readlist)
admin.site.register(Notes)
admin.site.register(Citation)