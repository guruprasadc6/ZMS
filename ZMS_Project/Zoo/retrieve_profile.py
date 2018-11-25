from .models import Animal,Department

def department_profile(item):
    depts = Department.objects.all().order_by('id')
    for key in depts:
        if(str(key)==item):
            return key