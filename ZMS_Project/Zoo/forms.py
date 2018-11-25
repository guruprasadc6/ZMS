from django import forms
from django.contrib.auth.models import User
from .models import Department,Exhibit,Animal,Staff,TicketBookings,LivesIn,WorksIn,Manages,LooksAfter,staff_test
from django.contrib.auth.forms import PasswordChangeForm


class ChangePassword(PasswordChangeForm):
    '''error_css_class = 'has-error'''''
    '''error_messages = {'password_incorrect':
                          "Το παλιό συνθηματικό δεν είναι σωστό. Προσπαθείστε   ξανά."}'''
    old_password = forms.CharField(required=True, label='Old password',
                             widget=forms.PasswordInput(attrs={
                                 'class': 'form-control','placeholder':'Old password'}),
                             )

    new_password1 = forms.CharField(required=True, label='New Password',
                              widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    new_password2 = forms.CharField(required=True, label='Re-enter New Password',
                              widget=forms.PasswordInput(attrs={
                                  'class': 'form-control','placeholder':'Enter Password'}),
                              )
    class Meta:
        model=User
        fields = ('old_password','new_password1','new_password2')

    def __init__(self,*args,**kwargs):
        super(ChangePassword,self).__init__(*args,**kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].label = ""
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter your Old Password'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].label = ""
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li> ' \
                                    '<li>Your password can\'t be a commonly used password.</li> <li>Your password can\'t be entirely numeric.</li> ' \
                                    ' </ul>'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter your New Password'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].label = ""
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Re-enter your New Password'
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class DepartmentForm(forms.ModelForm):
    id = forms.CharField(max_length=4, label="* Department ID",
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department ID'}))
    name = forms.CharField(max_length=45, label="* Department Name",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}))
    image = forms.ImageField(label='* Image')
    class Meta:
        model = Department
        fields = ['id','name','image']

class ExhibitForm(forms.ModelForm):
    id = forms.CharField(max_length=4, label="* Exhibit ID",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exhibit ID'}))
    name = forms.CharField(max_length=45, label="* Exhibit Name",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exhibit Name'}))
    # doo = forms.DateField(label="Date of Opening",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of Opening'}))


    doo = forms.DateField(label="* Date of opening",widget=forms.SelectDateWidget(years=range(1900,2100),attrs={'class': 'form-control'}))

    noofvisitors = forms.IntegerField(label="* No. of Visitors",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'No. of Visitors','type':'number'}))
    image = forms.ImageField(label='* Image')
    def clean_noofvisitors(self):
        no = self.cleaned_data['noofvisitors']
        if no<0:
            raise forms.ValidationError("Number of visitors can't be negative")
        return no

    class Meta:
        model = Exhibit
        fields = ['id', 'name','doo','noofvisitors','image']

class AnimalForm(forms.ModelForm):
    id = forms.CharField(max_length=4, label="* Animal ID",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Animal ID'}))
    commonname = forms.CharField(max_length=45, label="* Common Name",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Common Name'}))

    def clean_commonname(self):
        name  = self.cleaned_data['commonname']
        #print(fName)
        #print(type(fName))
        if not name.isalpha():
            #print('inside')
            raise forms.ValidationError("commonname should contain only alphabets")
        return name #return is IMPP

    scientificname = forms.CharField(max_length=45, label="* Scientific Name",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scientific Name'}))
    # dob = forms.DateField(label="Date of Birth",
    #                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}))

    dob = forms.DateField(label="* Date of birth",widget=forms.SelectDateWidget(attrs={'class': 'form-control'},years=range(1900,2100)))

    image = forms.ImageField(label='* Image')

    def clean_dob(self):
        date = self.cleaned_data['dob']

        present = date.today()

        if date > present:
            raise forms.ValidationError('Invalid date')
        return date

    class_field = forms.CharField(label="* Class field",max_length=45,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Common Name'}))
    # dod = forms.DateField(label="Date of Death",required=False,
    #                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of Death'}))

    # dod = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'},years=range(1900,2100)))
    #
    # def clean_dod(self):
    #     date = self.cleaned_data['dod']
    #
    #     present = date.today()
    #
    #     if date > present:
    #         raise forms.ValidationError('Invalid date')
    #     return date

    edscore = forms.FloatField(label="ED Score",required=False,
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ED Score'}))

    def clean_edscore(self):
        score = self.cleaned_data['edscore']
        if score==None:
            return score
        if score<0:
            raise forms.ValidationError("score can't be negative")
        return score

    height = forms.FloatField(label="* Height",
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'height'}))
    def clean_height(self):
        height = self.cleaned_data['height']
        if height<0:
            raise forms.ValidationError("height can't be negative")
        return height

    weight = forms.FloatField(label="* Weight",
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'weight'}))
    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight<0:
            raise forms.ValidationError("weight can't be negative")
        return weight

    healthstatus = forms.CharField(max_length=45, label="* Health Status",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Health Status'}))

    class Meta:
        model = Animal
        fields = ['id', 'commonname','scientificname','dob','class_field','edscore','height','weight','healthstatus','image']

class StaffForm(forms.ModelForm):
    id = forms.CharField(max_length=4, label="* Staff ID",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}))
    firstname = forms.CharField(max_length=45, label="* First Name",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    def clean_firstname(self):
        name  = self.cleaned_data['firstname']
        #print(fName)
        #print(type(fName))
        if not name.isalpha():
            #print('inside')
            raise forms.ValidationError("first name should contain only alphabets")
        return name #return is IMPP

    middlename = forms.CharField(max_length=45, label="Middle Name",required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}))

    def clean_middlename(self):
        name  = self.cleaned_data['middlename']
        #print(fName)
        #print(type(fName))
        if name=='':
            return name
        if not name.isalpha():
            #print('inside')
            raise forms.ValidationError("middle name should contain only alphabets")
        return name #return is IMPP

    lastname = forms.CharField(max_length=45, label="* Last Name",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    def clean_lastname(self):
        name  = self.cleaned_data['lastname']
        #print(fName)
        #print(type(fName))
        if not name.isalpha():
            #print('inside')
            raise forms.ValidationError("last name should contain only alphabets")
        return name #return is IMPP

    # dob = forms.DateField(label="Date of Birth",
    #                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}))
    image = forms.ImageField(label='* Image')
    dob = forms.DateField(label="* DOB",widget=forms.SelectDateWidget(attrs={'class':'form-control'},years=range(1900,2100)))

    def clean_dob(self):
        date = self.cleaned_data['dob']

        present = date.today()

        if date > present:
            raise forms.ValidationError('Invalid date')
        return date

    doorno = forms.CharField(max_length=45, label="Door No",required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Door No'}))
    housename = forms.CharField(max_length=45, label="House Name",required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House Name'}))
    streetname = forms.CharField(max_length=45, label="Street Name",required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name'}))

    # gender = forms.CharField(max_length=1, label="Gender",
    #                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gender'}))
    CHOICES = [('M', 'Male'), ('F', 'Female')]

    gender = forms.ChoiceField(label="* Gender",choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))

    contactno = forms.CharField(label="* Contact",max_length=10,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact No'}))
    def clean_contactno(self):
        contact = self.cleaned_data['contactno']
        if not (len(contact)==10 and contact.isdigit()):
            raise forms.ValidationError("Invalid phone number")
        return contact

    class Meta:
        model = Staff
        fields = ['id', 'firstname','middlename','lastname','dob','doorno','housename','streetname','gender','contactno','image']


# A CUSTOM FIELD
class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_name()



class LivesInForm(forms.ModelForm):
    CHOICES1 =(('1','2'),('2','3'),('4','5'))
    # CHOICES1 = [['1','2'],['2','3']]

    # animal_objects = list(Animal.objects.all())
    #CHOICES1 = [[str(ani.id),ani]  for ani in animal_objects ]
    # CHOICES2 = [[exh,exh.name] for exh in Exhibit.objects.all()]

    # animal = forms.CharField(widget=forms.Select(choices=CHOICES1))

    # animal = forms.ModelChoiceField(CHOICES1, required=True)
    # animal = forms.ModelChoiceField(Animal.objects ,required=True)

    animal = UserModelChoiceField(Animal.objects ,required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}, choices=Animal.objects.all())
                                  )
    # animal = forms.ModelChoiceField(CHOICES1, required=True)
    # exhibit= forms.CharField(widget=forms.Select(choices=CHOICES2))

    # exhibit = forms.ModelChoiceField(Exhibit.objects,required=True)
    exhibit = UserModelChoiceField(Exhibit.objects , required=True,
                                   widget=forms.Select(attrs={'class': 'form-control'}, choices=Exhibit.objects.all())
                                   )

    class Meta:
        model = LivesIn
        fields = ['animal','exhibit']



class WorksInForm(forms.ModelForm):
    staff = UserModelChoiceField(Staff.objects ,required=True,widget=forms.Select(attrs={'class':'form-control'},choices=Staff.objects.all()))
    dept = UserModelChoiceField(Department.objects , required=True,widget=forms.Select(attrs={'class':'form-control'},choices=Department.objects.all()))
    # widget = forms.Select(attrs={'class': 'form_control'}
    # staff = forms.ChoiceField(widget=UserModelChoiceField(S))
    # staff = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))


    doj = forms.DateField(widget=forms.SelectDateWidget(years=range(1900,2100), attrs={'class': 'form-control'}))
    def clean_doj(self):
        date = self.cleaned_data['doj']

        present = date.today()

        if date > present:
            raise forms.ValidationError('Invalid date')
        return date

    salary = forms.IntegerField(label='Salary', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}))
    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if salary<0:
            raise forms.ValidationError('Salary cannot be Zero')
        return salary

    class Meta:
        model = WorksIn
        fields = ['staff','dept','doj','salary']

class ManagesForm(forms.ModelForm):
    staff = UserModelChoiceField(Staff.objects, required=True,
                                 widget=forms.Select(attrs={'class': 'form-control'}, choices=Staff.objects.all()))
    exhibit = UserModelChoiceField(Exhibit.objects , required=True,
                                   widget=forms.Select(attrs={'class': 'form-control'}, choices=Exhibit.objects.all()))


    class Meta:
        model = Manages
        fields = ['staff','exhibit']


class LooksAfterForm(forms.ModelForm):
    staff = UserModelChoiceField(Staff.objects, required=True,
                                 widget=forms.Select(attrs={'class': 'form-control'}, choices=Staff.objects.all()))
    animal = UserModelChoiceField(Animal.objects , required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}, choices=Animal.objects.all()))

    class Meta:
        model = LooksAfter
        fields = ['staff','animal']




from django.core.validators import RegexValidator
#phone_validator = RegexValidator(r"\d{10}", "Phone number should contain only 10 digits.")
my_validator = RegexValidator(r"A", "Your string should contain letter A in it.")

'''class TicketBookingForm(forms.ModelForm):
    f_name = forms.CharField(max_length=200, label="First Name",
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name' ,'size':50})) # size is imPPP

    l_name = forms.CharField(max_length=200, label="Last Name",
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name','size':50}))
    age = forms.IntegerField(min_value=1 , max_value=100,label="Age",
                         widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age' ,'size':30}))  #NumberInput IMPPP
    #age = forms.CharField(label='Age' ,
     #                        widget=forms.IntegerField(min_value=1, max_value=100, label="Age",



    #gender = forms.CharField( widget=forms.RadioSelect(attrs= )
    CHOICES = [('M','Male'),('F','Female')]
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={
        'style': 'display: inline-block' }))

    #contact = forms.CharField(max_length=10 ,
    #                          widget=forms.TextInput(attrs={'type' :'' ,'class': 'form-control', 'placeholder': 'Phone ','size':50 }))

   # contact = forms.CharField(max_length=10 , widget= forms.RegexField("\d{10}") )
    contact = forms.CharField( validators=[my_validator] , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone' ,'size':30}))

    email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email' ,'size':30}))

    date_of_visit = forms.DateField(widget=  forms.SelectDateWidget())

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City' ,'size':30}))

    no_of_adult_tickets = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Adult Tickets' ,'size':30}))

    no_of_child_tickets = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Child Tickets' ,'size':30}))'''


class TicketBookingForm(forms.ModelForm):
    f_name = forms.CharField(max_length=200, label="First Name",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name',
                                                           'size': 50}))  # size is imPPP

    def clean_f_name(self):
        fName  = self.cleaned_data['f_name']
        #print(fName)
        #print(type(fName))
        if not fName.isalpha():
            #print('inside')
            raise forms.ValidationError("Name should contain only alphabets")
        return fName  #return is IMPP

    l_name = forms.CharField(max_length=200, label="Last Name",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Last Name', 'size': 50}))

    def clean_l_name(self):
        lName  = self.cleaned_data['l_name']
        if not lName.isalpha():
            print('inside')
            raise forms.ValidationError("Name should contain only alphabets")
        return lName



    age = forms.IntegerField(min_value=1, max_value=100, label="Age",
                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age',
                                                             'size': 30}))  # NumberInput IMPPP

    def clean_age(self):
        age = self.cleaned_data['age']
        if age<=0:
            raise forms.ValidationError("Age cannot be negative")
        return age

    CHOICES = [('M', 'Male'), ('F', 'Female')]
    # gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={
    #     'style': 'display: inline-block'}))

    gender = forms.ChoiceField(choices=CHOICES)


    contact = forms.CharField( max_length=10, label="Contact",widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone', 'size': 30}))


    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if not (len(contact)==10 and contact.isdigit()):
            raise forms.ValidationError("Invalid phone number")
        return contact

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'size': 30}))

    date_of_visit = forms.DateField(widget=forms.SelectDateWidget())

    def clean_date_of_visit(self):
        date = self.cleaned_data['date_of_visit']
        print(date)
        present = date.today()
        print(present)
        if date < present:
            raise forms.ValidationError('Invalid date')
        return date


    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'size': 30}))

    no_of_adult_tickets = forms.IntegerField(min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Adult Tickets', 'size': 30}))
    def clean_no_of_adult_tickets(self):
        n = self.cleaned_data['no_of_adult_tickets']
        if n<0:
            raise forms.ValidationError('Only Positive Values')
        return n

    no_of_child_tickets = forms.IntegerField(min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Child Tickets', 'size': 30}))

    def clean_no_of_child_tickets(self):
        n = self.cleaned_data['no_of_child_tickets']
        if n<0:
            raise forms.ValidationError('Only Positive Values')
        return n



    class Meta:
        model = TicketBookings
        fields = ['f_name','l_name','age', 'gender','contact','email','date_of_visit','city','no_of_adult_tickets','no_of_child_tickets']
        #fields = ['f_name', 'l_name','age','gender','contact']




class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=20, label="* Username",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),required=True)
    password = forms.CharField(max_length=20, label= "* Password",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),required=True)
    email = forms.EmailField(label="* Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'size': 30}), required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = staff_test
        fields = ('cardid',)


class FeedBackFrom(forms.Form):
    name = forms.CharField(max_length=200, label="Name",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name',
                                                           'size': 50}), required=True)  # size is imPPP
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'size': 30}), required=True)
    CHOICES = [('India', 'India'), ('USA', 'USA')]

    country = forms.ChoiceField(choices=CHOICES,required=True)

    fb = forms.ChoiceField(widget=forms.Textarea, required=True)