from django.shortcuts import render,redirect
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'index.html')

def sindex(request):
    return render(request, 'sindex.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "Email already exist!!"
            return render(request, 'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['confirm_password']:
                User.objects.create(
                    email = request.POST['email'],
                    mobile = request.POST['mobile'],
                    name = request.POST['name'],
                    password = request.POST['password'],
                    uprofile = request.FILES['uprofile'],
                    usertype = request.POST['usertype']
                )
                msg1 = "Signup Successfully!"
                return render(request, 'signup.html',{'msg1':msg1})
            else:
                msg = "Password & confirm password does not match!"
                return render(request, 'signup.html',{'msg':msg})
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])    
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['uprofile'] = user.uprofile.url
                request.session['name'] = user.name
                if user.usertype == 'buyer':
                    return redirect('index')
                else:
                    return redirect('sindex')
            else:
                msg = "password does not match!"
                return render(request, 'login.html', {'msg':msg})
        except:
            msg = "Email does not exist!"
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')
    
def logout(request):
    del request.session['email']
    del request.session['uprofile']
    return redirect('login')

def fpass(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            subject = 'OTP for forget-password'
            otp = random.randint(1001, 9999)
            message = 'Hello ' + user.name+ ' your otp  for forgot password so please verify this otp and your otp is : '+str(otp) 
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject,message,email_from,recipient_list)
            request.session['email'] = user.email
            request.session['otp'] = otp
            return render(request, 'otp.html')
        except:
            msg = "Email does not exist!!"
            return render(request, 'fpass.html',{'msg':msg})
    else: 
        return render(request, 'fpass.html')
    
def otp(request):
    if request.method == 'POST':
        try:
            otp = int(request.session['otp'])
            uotp = int(request.POST['uotp'])
            if otp == uotp:
                del request.session['otp']
                return redirect('newpass')
            else:
                msg = "Invalid otp!"
                return render(request, 'otp.html', {'msg':msg})
        except:
            pass
    else:
        return render(request, 'otp.html')

def newpass(request):
   if request.method == 'POST':
        try:
            user = User.objects.get(email = request.session['email'])
            if request.POST['npassword'] == request.POST['cnpassword']:
                user.password = request.POST['npassword']
                user.save()
                del request.session['email']
                return redirect('login')
            else:
                msg = "New password & confirm new password does not match!!"
                return render(request, 'newpass.html',{'msg':msg})
        except Exception as e:
             #print("****",e)
             msg = "Session expired or user not found!"
             return render(request, 'fpass.html', {'msg': msg})
   else:
       return render(request, 'newpass.html')
   
def cpass(request):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email = request.session['email'])
    if request.method == "POST":
        try:
            if user.password == request.POST['opassword']:
                if request.POST['npassword'] == request.POST['cnpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    return redirect('logout')
                else:
                    msg = "new password & confirm new password does not match!!"
                    if user.usertype == 'buyer':
                        return render(request, 'cpass.html',{'msg':msg})
                    else:
                        return render(request, 'scpass.html',{'msg':msg})
            else:
                msg = "Old password does not match!!"
                if user.usertype == 'buyer':
                    return render(request, 'cpass.html',{'msg':msg})
                else:
                    return render(request, 'scpass.html',{'msg':msg})
        except:
            pass
    else:
        if user.usertype == 'buyer':
            return render(request, 'cpass.html')
        else:
            return render(request, 'scpass.html')

def profile(request):
    user = User.objects.get(email = request.session['email'])
    if request.method == 'POST':
        user.name = request.POST['name']
        user.mobile = request.POST['mobile']
        try:
            user.uprofile = request.FILES['uprofile']
            user.save()
            request.session['uprofile'] = user.uprofile.url  # session updated...
        except:
            pass
        user.save()
        if user.usertype == 'buyer':
            return redirect('index')
        else:
            return redirect('sindex')
    else:
        return render(request, 'profile.html', {'user':user})
    
def add_product(request):
    user = User.objects.get(email = request.session['email'])
    if request.method == 'POST':
        try:
            Product.objects.create(
                user = user,
                pcategory = request.POST['pcategory'],
                pcompany = request.POST['pcompany'],
                pname = request.POST['pname'],
                pprice = request.POST['pprice'],
                pdesc = request.POST['pdesc'],
                pimage = request.FILES['pimage']
            )
            msg1 = "Product added Successfuly!"
            return render(request, 'add_product.html', {'msg1':msg1})
        except Exception as e:
            print("*****",e)
            msg = "Invalid details for product!"
            return render(request, 'add_product.html', {'msg':msg})
    else:
        return render(request, 'add_product.html')

def view_product(request):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.filter(user=user)
    return render(request, 'view_product.html', {'product': product})

def single(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    return render(request, 'single.html', {'product':product})

def edit_product(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    if request.method == 'POST':
        product.pname = request.POST['pname']
        product.pprice = request.POST['pprice']
        product.save()
        return redirect('view_product')
    else:
        return render(request, 'edit_product.html', {'product':product})
    
def delete(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    product.delete()
    return redirect('view_product')

def Error(request):
    return render(request, 'Error.html')

def bestseller(request):
    return render(request, 'bestseller.html')

def cheackout(request):
    return render(request, 'cheackout.html')

def shop(request):
    return render(request, 'shop.html')

def cart(request):
    return render(request, 'cart.html')