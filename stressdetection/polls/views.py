from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from urllib import request
from django.http import  JsonResponse
from django.shortcuts import render, redirect
from .models import newuser,student,Contact

from django.contrib import messages


def navbar(request):
    return render(request, 'base.html')




def user_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        pass1 = request.POST['pass1']

        # Check if the Aadhaar number and password match an existing student
        student = newuser.objects.filter(Username=Username, pass1=pass1).first()
        if student:
            # Set the student ID in the session to keep the student logged in
            request.session['student_id'] = student.id
            return redirect('userhome')

        return render(request, 'login.html', {'error': 'Invalid username number or password'})

    # return render(request, 'login.html')
    return render(request,'login.html')




def user_registration(request):
    if request.method == 'POST':
        Username=request.POST['Username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if newuser.objects.filter(Username=Username).exists():
            messages.warning(request,'Username is already exists')
            return redirect('registration')
        else:
            newuser(Username=Username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2).save()
            messages.success(request, 'The new user '+request.POST['Username']+ " IS saved successfully..!")
            return redirect('user_login')
    else:
         return render(request,'register.html')


def logout(request):
    # logout(request)
    messages.success(request,"successfully logout..!")
    return redirect('navbar')

def userhome(request):
    return render(request,'user_home.html')



def admin_login(request):
    if request.method== 'POST':
        try:
            Userdetailes=student.objects.get(Username=request.POST['Username'], pass1=request.POST['pass1'])
            print("Username=",Userdetailes)
            request.session['Username']=Userdetailes.Username
            messages.success(request,"successfully login")
            return redirect('admin_home')
        except student.DoesNotExist as e:   
            messages.error(request,"Username/ Password Invalied...!")
   
    return render(request,'admin_login.html')


def admin_registration(request):
    if request.method == 'POST':
        Username=request.POST['Username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if student.objects.filter(Username=Username).exists():
            messages.warning(request,'Username is already exists')
            return redirect('admin_registration')
        else:
            student(Username=Username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2).save()
            messages.success(request, 'The new user '+request.POST['Username']+ " IS saved successfully..!")
            return redirect('admin_login')
    else:
         return render(request,'admin_register.html')


def admin_logout(request):
    # logout(request)
    messages.success(request,"successfully logout..!")
    return redirect('navbar')



def admin_home(request):
    return render(request,'admin_home.html')




def user_contact(request):
    if request.method=='POST':
        names=request.POST['names']
        email=request.POST['email']
        phone=request.POST['phone']
        desc=request.POST['desc']
        contacts= Contact(names=names,email=email,phone=phone,desc=desc)
        contacts.save()    
        return redirect('user_contact')
    else:
        return render(request,'user_contact.html')


def user_about(request):
    return render(request,'about.html')



def view_user(request):
    form=newuser.objects.all()
    return render(request,'view_user.html' , {'forms':form})