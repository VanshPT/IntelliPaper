from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ResearchPaper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=1000)
    abstract = models.TextField()
    pdf_file = models.FileField(upload_to='pdfs/')
    extracted_text = models.TextField(blank=True)
    upload_datetime = models.DateTimeField(auto_now_add=True, null=True )

    def __str__(self):
        return self.title

class Citation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, null=True, blank=True)
    citations = models.TextField()

    def __str__(self):
        return self.paper.title
    
class VectorDocument(models.Model):
    paper=models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    document = models.TextField()
    vector_representation = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vector for {self.paper.title}"
    
    
class Folder(models.Model):
    name = models.CharField(max_length=255)
    papers = models.ManyToManyField(ResearchPaper, related_name='folders')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Readlist(models.Model):
    name = models.CharField(max_length=255)
    papers = models.ManyToManyField(ResearchPaper, related_name='readlists')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Notes for {self.paper.title} by {self.user.username}'