from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import DepartmentForm,ExhibitForm,AnimalForm,StaffForm,TicketBookingForm,LivesInForm,WorksInForm,ManagesForm,LooksAfterForm,UserForm,UserProfileForm,ChangePassword,FeedBackFrom
from .models import Animal,Department,Staff,Exhibit,WorksIn,LivesIn,Manages,LooksAfter
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_list_or_404, get_object_or_404

from django.contrib.auth.models import User

import pymongo
import requests
import matplotlib.pyplot as plt

import re

from django.db import connection

# Create your views here.
def home(request):
    # return render(request,'Zoo/home.html',{})
    return  render(request,'Zoo/home.html',{})


def login_user(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Logged in successfully')
            return redirect('home')
        else:
            messages.success(request,'Failed to Log in! Try again...')
            return redirect('login')
    else:
        return render(request, 'Zoo/login.html', {})
def logout_user(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('home')

@login_required(login_url='/permissionError/')
def change_password(request):
    if (request.method == 'POST'):
        form = ChangePassword(data=request.POST,user=request.user)
        if (form.is_valid()):
            form.save()
            messages.success(request, 'You have successfully changed your password')
            return redirect('home')
    else:
        form = ChangePassword(user=request.user)
    context = {'form': form}
    return render(request, 'zoo/change_password.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def add_department(request):
    if (request.method == 'POST'):
        form = DepartmentForm(request.POST, request.FILES)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
            return redirect('department_list')
        else:
            print (form.errors)
    else:
        form = DepartmentForm()
    context = {'form':form}
    return render(request,'Zoo/add_department.html',context)

@login_required(login_url='/permissionError/')
def add_exhibit(request):
    if (request.method == 'POST'):
        form = ExhibitForm(request.POST, request.FILES)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
            return redirect('exhibit_list')
        else:
            print (form.errors)
    else:
        form = ExhibitForm()
    context = {'form':form}
    return render(request,'Zoo/add_exhibit.html',context)

@login_required(login_url='/permissionError/')
def add_animal(request):
    if (request.method == 'POST'):
        form = AnimalForm(request.POST, request.FILES)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
            return redirect('view_animals')
        else:
            print (form.errors)
    else:
        form = AnimalForm()
    context = {'form':form}
    return render(request,'Zoo/add_animal.html',context)

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
# Im using register to add staff
def add_staff(request):
    # if (request.method == 'POST'):
    #     form = StaffForm(request.POST, request.FILES)# instance=request.user)
    #     if(form.is_valid()):
    #         form.save(commit=True)
    #         messages.success(request, 'You have successfully added a record')
    #         return redirect('staff_list')
    #     else:
    #         print (form.errors)
    # else:
    #     form = StaffForm()
    # context = {'form':form}
    # return render(request,'Zoo/add_Staff.html',context)
    if request.method == "POST":
        form = StaffForm(request.POST, request.FILES)  # instance=request.user)
        if (form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
            return redirect('staff_list')
        else:
            print(form.errors)
    else:
        form = StaffForm()
    context = {'form': form}
    return render(request, 'Zoo/add_staff.html', context)

@login_required(login_url='/permissionError/')
def view_animals(request):
    animals = ""
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''

    # Raw SQL Queries

    # res = Animal.objects.raw('SELECT id,commonname  FROM animal WHERE height>50 ')
    # for a in res:
    #     print(a.id,a.commonname)
    #
    # print('----------')
    # res =WorksIn.objects.raw('SELECT * FROM works_in WHERE works_in.dept_id= %s AND works_in.salary> %s ',[0000,1000])
    # for a in res:
    #     print(a.staff_id)

    # related to department
    max_salary, min_salry , avg_salary = get_max_and_min_salary('0000')
    emp_count = get_emp_count('0000')




    animals = Animal.objects.filter(commonname__contains=search_text) or Animal.objects.filter(id__contains=search_text)
    return render(request, 'Zoo/list_animals.html', {'animals': animals})

@login_required(login_url='/permissionError/')
def animal_profile(request,id):
    key = Animal.objects.get(pk=id)
    context = {'key':key}
    if str(key.image)!='':
        url = '../../static/Zoo/media/' + str(key.image)[2:-1]
        context['url'] = url

    id = key.id
    # Animal exhibit and staff looking after it
    exhibit, staffs = get_animal_relations(id)
    context['exhibit'] = exhibit
    context['staffs'] = staffs

    return render(request, 'Zoo/animal_profile.html', context)

@login_required(login_url='/permissionError/')
def animal_delete(request, id):
    animal = Animal.objects.get(pk = id)
    animal.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('view_animals')

@login_required(login_url='/permissionError/')
def edit_animal(request, id):
   animal = get_object_or_404(Animal, pk=id)
   if request.method == "POST":
       form = AnimalForm(request.POST,request.FILES, instance=animal)
       if form.is_valid():
          post = form.save(commit=True)
          post.save()
          return redirect('view_animals')
   else:
       form = AnimalForm(instance=animal)
   return render(request, 'Zoo/edit_animal.html', {'form': form,'animal':animal})

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def deptList(request):
    depts = ""
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    depts = Department.objects.filter(name__contains=search_text) or Department.objects.filter(id__contains=search_text)
    return render(request, 'Zoo/department_list.html', {'depts': depts})
    #depts = Department.objects.all().order_by('id')
    #return render(request,'Zoo/department_list.html',{'depts':depts})

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def delete(request, id):
    department = Department.objects.get(pk = id)
    department.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('department_list')
    #return render(request,'Zoo/department_list.html',{'depts':depts})

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def edit_department(request, id):
   department = get_object_or_404(Department, pk=id)
   if request.method == "POST":
       form = DepartmentForm(request.POST,request.FILES, instance=department)
       if form.is_valid():
          # post = form.save(commit=True)
          post = form.save()
          post.save()
          return redirect('department_list')
   else:
       form = DepartmentForm(instance=department)
   return render(request, 'Zoo/edit_department.html', {'form': form,'dept':department})

'''def search_department(request):
    depts=""
    if(request.method=='POST'):
        search_text = request.POST['search_text']
    else:
        search_text=''
    depts = Department.objects.filter(name__contains=search_text ) or Department.objects.filter(id__contains=search_text )
    return render(request,'Zoo/department_search.html',{'depts':depts})'''

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def department_profile(request,id):
    key = Department.objects.get(pk=id)
    context = {'key':key}

    id = key.id
    max_salary, min_salary,avg_salary = get_max_and_min_salary(id)
    emp_count = get_emp_count(id)

    context['min_salary'] = min_salary
    context['max_salary'] = max_salary
    context['avg_salary'] = avg_salary
    context['emp_count'] = emp_count



    if str(key.image)!='':
        url = '../../static/Zoo/media/' + str(key.image)[2:-1]
        context['url'] = url
    return render(request, 'Zoo/department_profile.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def view_staff(request):
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    staff = Staff.objects.filter(firstname__contains=search_text) or Staff.objects.filter(lastname__contains=search_text)or Staff.objects.filter(id__contains=search_text)
    return render(request, 'Zoo/staff_list.html', {'staff': staff})

@login_required(login_url='/permissionError/')
def staff_profile(request,id):
    key = Staff.objects.get(pk=id)
    context = {'key':key}
    if str(key.image)!='':
        url = '../../static/Zoo/media/' + str(key.image)[2:-1]
        context['url'] = url

    # Relations
    id = key.id
    animals, exhibits ,department_name,salary,doj = get_staff_relations(id)

    context['animals'] = animals
    context['exhibits'] = exhibits
    context['department_name']= department_name
    context['salary']= salary
    context['doj']=doj

    return render(request, 'Zoo/staff_profile.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def staff_delete(request, id):
    staff = Staff.objects.get(pk = id)
    user_name = staff.user
    print('user_name', user_name)
    del_user(user_name)
    staff.delete()
    messages.success(request, 'Deleted successfully')



    return redirect('staff_list')

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def edit_staff(request, id):
   staff = get_object_or_404(Staff, pk=id)
   if request.method == "POST":
       form = StaffForm(request.POST,request.FILES,instance=staff)
       if form.is_valid():
          post = form.save()
          post.save()
          return redirect('staff_list')
   else:
       form = StaffForm(instance=staff)
   return render(request, 'Zoo/edit_staff.html', {'form': form,'staff':staff})

@login_required(login_url='/permissionError/')
def view_exhibit(request):
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    exhibit = Exhibit.objects.filter(name__contains=search_text) or Exhibit.objects.filter(id__contains=search_text)
    return render(request, 'Zoo/exhibit_list.html', {'exhibits': exhibit})

@login_required(login_url='/permissionError/')
def exhibit_profile(request,id):
    key = Exhibit.objects.get(pk=id)
    context = {'key':key}
    if str(key.image)!='':
        url = '../../static/Zoo/media/' + str(key.image)[2:-1]
        context['url'] = url

    staffs, animals = get_exhibit_relations(key.id)
    context['staffs'] = staffs
    context['animals'] = animals
    return render(request, 'Zoo/exhibit_profile.html', context)

@login_required(login_url='/permissionError/')
def exhibit_delete(request, id):
    exhibit = Exhibit.objects.get(pk = id)
    exhibit.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('exhibit_list')

@login_required(login_url='/permissionError/')
def edit_exhibit(request, id):
   exhibit= get_object_or_404(Exhibit, pk=id)
   if request.method == "POST":
       form = ExhibitForm(request.POST, request.FILES,instance=exhibit)
       if form.is_valid():
          post = form.save(commit=True)
          post.save()
          return redirect('exhibit_list')
   else:
       form = ExhibitForm(instance=exhibit)
   return render(request, 'Zoo/edit_exhibit.html', {'form': form,'exhibits':exhibit})

def sidebar(request):
    return render(request,'Zoo/Sidebar.html',{})
def test(request):
    return render(request, 'Zoo/test.html', {})






def book_ticket(request):
    args = {}
    if request.POST:
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            args['name'] = form.cleaned_data.get('f_name')
            args['n1'] = form.cleaned_data.get('no_of_adult_tickets')
            args['n2'] = form.cleaned_data.get('no_of_child_tickets')
            args['price1'] = 100 * form.cleaned_data.get('no_of_adult_tickets')
            args['price2'] = 50 * form.cleaned_data.get('no_of_child_tickets')
            args['total'] = args['price1']+args['price2']
            form.save()



            print('success')
            return render(request, 'Zoo/ticket_bill.html', args)


    else:
        # print("error")
        form = TicketBookingForm()


    args['form']  = form
    return render(request,'Zoo/bookTickets.html',args)

def ticket_bill(request):
    return  None



def feedback(request):
    form = FeedBackFrom()
    return render(request, 'Zoo/feedback.html', {'form':form})





def calc_feedback_score(text):
    subscription_key = "2292fabc461849e2ad69949ede7ea881"
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"




    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    sentiment_api_url = text_analytics_base_url + "sentiment"

    print(sentiment_api_url)

    documents = {'documents': [
        {'id': '1', 'language': 'en', 'text': text}]}

    response = requests.post(sentiment_api_url, headers=headers, json=documents, verify=False)
    sentiments = response.json()

    print(sentiments['documents'][0]['score'])

    return sentiments['documents'][0]['score']

def add_Feedback(request):

    if request.method == 'POST':
        print('insid POST')
        form = FeedBackFrom(request.POST)
        print('after getting')

        # cd = form.cleaned_data
        # # now in the object cd, you have the form as a dictionary.
        # comment = cd.get('fb')
        # print('comment', comment)
        # name = cd.get('name')
        # emailid = cd.get('email')
        # country = cd.get('country')
        comment = request.POST['fb']
        name = request.POST['name']
        emailid = request.POST['email']
        country = request.POST['country']

        score = calc_feedback_score(comment)


        mydict = {'fb':comment,'score':score,'name':name,'email':emailid,'country':country}

        # establishing connection
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        # selecting db
        mydb = myclient['Feedback']

        # selecting collection(table)
        mycol = mydb["feedbackCollection"]

        mycol.insert_one(mydict)

        myclient.close()

        return redirect('home')
        return redirect('home')

    else:
        form = FeedBackFrom()
        return render(request, 'Zoo/feedback.html', {'form':form})





def draw_pie_chart(S,B,F):
    labels = 'Excellent', 'Average', 'Bad'
    sizes = [S,B,F]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('Zoo/static/Zoo/pie')

@login_required(login_url='/permissionError/')
def pie_chart(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient['Feedback']

    mycol = mydb["feedbackCollection"]

    S , B , F = 0, 0, 0
    for record in mycol.find():
        if record['score']>0.8:
            S+=1
        elif record['score']>0.4:
            B+=1
        else:
            F+=1

    draw_pie_chart(S,B,F)


    myclient.close()

    return render(request,'Zoo/pie_chart.html',{})



@login_required(login_url='/permissionError/')
def lives_in(request):
    # animals = Animal.objects.all().order_by('id')
    # exhibits = Exhibit.objects.all().order_by('id')
    # return render(request,'Zoo/department_list.html',{'animals':animals,'exhibits':exhibits})


    if (request.method == 'POST'):
        form = LivesInForm(request.POST)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
        else:
            print (form.errors)
    else:
        form = LivesInForm()
    context = {'form':form}
    return render(request,'Zoo/lives_in.html',context)

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def works_in(request):

    if (request.method == 'POST'):
        form = WorksInForm(request.POST)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
        else:
            print (form.errors)
    else:
        form = WorksInForm()
    context = {'form':form}
    return render(request,'Zoo/works_in.html',context)

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def manages(request):

    if (request.method == 'POST'):
        form = ManagesForm(request.POST)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
        else:
            print (form.errors)
    else:
        form = ManagesForm()
    context = {'form':form}
    return render(request,'Zoo/manages.html',context)


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def looks_after(request):

    if (request.method == 'POST'):
        form =LooksAfterForm(request.POST)# instance=request.user)
        if(form.is_valid()):
            form.save(commit=True)
            messages.success(request, 'You have successfully added a record')
        else:
            print (form.errors)
    else:
        form = LooksAfterForm()
    context = {'form':form}
    return render(request,'Zoo/looks_after.html',context)


def get_max_and_min_salary(id):
    with connection.cursor() as cursor:

        # cursor.execute('SELECT * FROM animal')

        cursor.execute('SELECT MAX(salary), MIN(salary), AVG(salary) FROM works_in WHERE dept_id = %s',[id])
        res = cursor.fetchone()


        cursor.close()
        print(res)
        return res


def get_emp_count(id):
    with connection.cursor() as cursor:

        cursor.execute('SELECT COUNT(*) FROM works_in WHERE dept_id = %s',[id])
        res = cursor.fetchone()

        cursor.close()
        print(res)
        return res[0]

def get_animal_relations(id):
    with connection.cursor() as cursor:

        exhibit,staffs = None,None
        cursor.execute('SELECT  e.name  FROM lives_in AS l,exhibit AS e WHERE l.animal_id = %s AND l.exhibit_id = e.id ',[id])
        exhibit = cursor.fetchone()
        try:
            exhibit = exhibit[0]
        except:
            pass

        cursor.execute('SELECT  s.firstName  FROM looks_after AS l,staff AS s WHERE l.animal_id = %s AND l.staff_id = s.id ', [id])
        staffs = cursor.fetchall()

        # clean staffs
        if staffs:
            _ = []
            for row in staffs:
                _.append(row[0])
            staffs = _
        else:
            staffs = None


        cursor.close()
        print(exhibit,staffs)
        return exhibit,staffs

def get_staff_relations(id):
    with connection.cursor() as cursor:
        exhibits, animals = None,None
        cursor.execute('SELECT  e.name  FROM manages AS m,exhibit AS e WHERE m.staff_id = %s AND m.exhibit_id = e.id ',[id])
        exhibits = cursor.fetchall()

        cursor.execute('SELECT  a.commonname FROM looks_after AS l,animal AS a WHERE l.staff_id = %s AND l.animal_id = a.id ', [id])
        animals = cursor.fetchall()

        cursor.execute('SELECT  d.name , w.salary, w.doj FROM works_in as w,department as d where w.staff_id =%s and w.dept_id = d.id', [id])
        department = cursor.fetchall()
        # print(department[0])
        department_name,salary,doj = None,None,None
        try:
            department_name,salary,doj = department[0]
        except:
            pass
        cursor.close()


        # clean animals
        if animals:
            animals_cleaned = []
            for row in animals:
                animals_cleaned.append(row[0])
            animals = animals_cleaned
        else:
            animals=  None

        # clean exhibits
        if exhibits:
            exhibits_cleaned = []
            for row in exhibits:
                exhibits_cleaned.append(row[0])
            exhibits =exhibits_cleaned
        else:
            exhibits=None

        print(exhibits, '|', animals, '|', department_name, salary, doj)

        return animals,exhibits,department_name,salary,doj

def get_exhibit_relations(id):
    with connection.cursor() as cursor:
        staffs,animals = None,None
        cursor.execute('SELECT  s.firstname  FROM manages AS m,staff AS s WHERE m.exhibit_id = %s AND m.staff_id = s.id ',
                       [id])
        staffs = cursor.fetchall()
        # clean staffs
        if staffs:
            _ = []
            for row in staffs:
                _.append(row[0])
            staffs = _
        else:
            staffs = None

        cursor.execute(
            'SELECT  a.commonname FROM lives_in AS l,animal AS a WHERE l.exhibit_id = %s AND l.animal_id = a.id ',
            [id])
        animals = cursor.fetchall()

        # clean animals
        if animals:
            _ = []
            for row in animals:
                _.append(row[0])
            animals = _
        else:
            animals =None

        print(staffs, animals)

        return staffs,animals



@login_required(login_url='/permissionError/')
def view_lives_in(request):
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    lives_in_objects = LivesIn.objects.filter(animal__commonname__contains=search_text ) or  LivesIn.objects.filter(exhibit__name__contains=search_text)
    # lives_in_objects = LivesIn.objects.all()

    print(lives_in_objects, len(lives_in_objects))
    for l in lives_in_objects:
        print(l.id)
        print(l.animal.id , l.exhibit.id)



    return render(request, 'Zoo/list_lives_in.html', {'lives_in_objects':lives_in_objects })

@login_required(login_url='/permissionError/')
def lives_in_profile(request,id):
    key = LivesIn.objects.get(pk=id)
    context = {'key':key}


    id = key.id


    return render(request, 'Zoo/lives_in_profile.html', context)

@login_required(login_url='/permissionError/')
def edit_lives_in(request, id):
   lives_in = get_object_or_404(LivesIn, pk=id)
   if request.method == "POST":
       form = LivesInForm(request.POST, instance=lives_in)
       if form.is_valid():
          post = form.save(commit=True)
          post.save()
          return redirect('list_lives_in')
   else:
       form = LivesInForm(instance=lives_in)
   return render(request, 'Zoo/edit_lives_in.html', {'form': form,'lives_in':lives_in})

@login_required(login_url='/permissionError/')
def delete_lives_in(request, id):
    lives_in = LivesIn.objects.get(pk = id)
    lives_in.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('list_lives_in')














def register(request):
    registered = False
    print('inside register')
    if request.method == 'POST':
        print('inside POST')
        user_form = UserForm(request.POST,request.FILES)
        profile_form = StaffForm(request.POST,request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            print('inside valid')
            if not bool(re.search("@", request.POST['email'])):
                return HttpResponse("Enter valid email-id.")

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # name = user.username
            # cID = profile.cardid

            registered = True
            # connectionObject = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)

            # try:
            #
            #     cursorObject = connectionObject.cursor()
            #     cursorObject.execute("INSERT INTO customer (cardID,customerName) VALUES (%s,%s)", [cID, name])
            #     connectionObject.commit()
            #
            #     cursorObject.execute("INSERT INTO customerinshop (cardID) VALUES (%s)", [cID])
            #     connectionObject.commit()
            #
            # except Exception as e:
            #
            #     print("Exeception occured:{}".format(e))
            # finally:
            #     connectionObject.close()
            #     pass
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = StaffForm()

    return render(request,
                  'Zoo/add_Staff.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                  )





def del_user( user_name):
    try:
        u = User.objects.get(username = user_name)
        u.delete()
        print("The user is deleted")

    except User.DoesNotExist:
       print("User doesnot exist")



@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def view_works_in(request):
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    works_in_objects = WorksIn.objects.filter(staff__firstname__contains=search_text ) or WorksIn.objects.filter(staff__lastname__contains = search_text)  or WorksIn.objects.filter(dept__name__contains=search_text)
    # works_in_objects = WorksIn.objects.all()

    print(works_in_objects, len(works_in_objects))
    for w in works_in_objects:
        print(w.id)
        print(w.staff.id , w.dept.id)



    return render(request, 'Zoo/list_works_in.html', {'works_in_objects':works_in_objects })


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def works_in_profile(request,id):
    key = WorksIn.objects.get(pk=id)
    context = {'key':key}
    return render(request, 'Zoo/works_in_profile.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def edit_works_in(request, id):
   works_in = get_object_or_404(WorksIn, pk=id)
   if request.method == "POST":
       form = WorksInForm(request.POST, instance=works_in)
       if form.is_valid():
          post = form.save(commit=True)
          post.save()
          return redirect('list_works_in')
   else:
       form = WorksInForm(instance=works_in)
       print(form)
   return render(request, 'Zoo/edit_works_in.html', {'form': form,'works_in':works_in})

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def delete_works_in(request, id):
    works_in = WorksIn.objects.get(pk = id)
    works_in.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('list_works_in')



@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def view_looks_after(request):
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    looks_after_objects = LooksAfter.objects.filter(staff__firstname__contains=search_text ) or LooksAfter.objects.filter(staff__lastname__contains = search_text)  or LooksAfter.objects.filter(animal__commonname__contains=search_text)
    # looks_after_objects = LooksAfter.objects.all()

    print(looks_after_objects, len(looks_after_objects))
    for l in looks_after_objects:
        print(l.id)
        print(l.staff.id , l.animal.id)



    return render(request, 'Zoo/list_looks_after.html', {'looks_after_objects':looks_after_objects })

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def looks_after_profile(request,id):
    key = LooksAfter.objects.get(pk=id)
    context = {'key':key}
    return render(request, 'Zoo/looks_after_profile.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def edit_looks_after(request, id):
   looks_after = get_object_or_404(LooksAfter, pk=id)
   if request.method == "POST":
       form = LooksAfterForm(request.POST, instance=looks_after)
       if form.is_valid():
          post = form.save(commit=True)
          post.save()
          return redirect('list_looks_after')
   else:
       form = LooksAfterForm(instance=looks_after)
       print(form)
   return render(request, 'Zoo/edit_looks_after.html', {'form': form,'looks_after':looks_after})

@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def delete_looks_after(request, id):
    looks_after = LooksAfter.objects.get(pk = id)
    looks_after.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('list_looks_after')


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def view_manages(request):
    if (request.method == 'POST'):
        search_text = request.POST['search_text']
    else:
        search_text = ''
    manages_objects = Manages.objects.filter(staff__firstname__contains=search_text ) or Manages.objects.filter(staff__lastname__contains = search_text)  or Manages.objects.filter(exhibit__name__contains=search_text)
    # manages_objects = Manages.objects.all()
    # print(manages_objects[0].exhibit.id)
    print(manages_objects, len(manages_objects))
    for m in manages_objects:
        print(m.id)
        print(m.staff, m.exhibit.id)



    return render(request, 'Zoo/list_manages.html', {'manages_objects':manages_objects })


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def manages_profile(request,id):
    key = Manages.objects.get(pk=id)
    context = {'key':key}
    return render(request, 'Zoo/manages_profile.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def edit_manages(request, id):
   manages = get_object_or_404(Manages, pk=id)
   if request.method == "POST":
       form = ManagesForm(request.POST, instance=manages)
       if form.is_valid():
          post = form.save(commit=True)
          post.save()
          return redirect('list_manages')
   else:
       form = ManagesForm(instance=manages)
       print(form)
   return render(request, 'Zoo/edit_manages.html', {'form': form,'manages':manages})


@user_passes_test(lambda u: u.is_superuser, login_url='/permissionError/')
def delete_manages(request, id):
    manages = Manages.objects.get(pk = id)
    manages.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('list_manages')


def permissionError(request):
    return render(request, 'Zoo/permissionError.html', {})

def animal_gallery(request):
    return render(request, 'Zoo/gallery/animal_gallery.html', {})
def bird_gallery(request):
    return render(request, 'Zoo/gallery/bird_gallery.html', {})
def aquatic_gallery(request):
    return render(request, 'Zoo/gallery/aquatic_gallery.html', {})