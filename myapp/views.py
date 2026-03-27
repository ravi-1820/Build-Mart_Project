from django.shortcuts import render,redirect
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    product = Product.objects.all()
    return render(request, 'index.html', {'product':product})

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

# @csrf_exempt
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
        if request.POST.get('pcategory') and request.POST.get('pcategory') != 'category':
            product.pcategory = request.POST['pcategory']
        if request.POST.get('pcompany') and request.POST.get('pcompany') != 'company':
            product.pcompany = request.POST['pcompany']
        product.pname = request.POST['pname']
        product.pprice = request.POST['pprice']
        product.pdesc = request.POST['pdesc']
        if 'pimage' in request.FILES:
            product.pimage = request.FILES['pimage']
        product.save()
        return redirect('view_product')
    else:
        return render(request, 'edit_product.html', {'product':product})
    
def delete(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    product.delete()
    return redirect('view_product')

def add_wishlist(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    try:
        Wishlist.objects.create(
            user = user,
            product = product
        )
    except:
        pass
    return redirect('wishlist')

def wishlist(request):
    user = User.objects.get(email = request.session['email'])
    wish = Wishlist.objects.filter(user = user)
    return render(request, 'wishlist.html', {'wish':wish})

def delete_wishlist(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk=pk)
    try:
        Wishlist.objects.filter(user=user, product=product).delete()
    except:
        pass
    return redirect('wishlist')

def b_single(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    signal = False
    try:
        if Wishlist.objects.filter(user=user, product=product).exists():
            signal = True
    except:
        pass
    return render(request, 'b_single.html', {'product':product, 'signal':signal})

def add_cart(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    try:
        Cart.objects.create(
            user = user,
            product = product,
            total = product.pprice,
            qty = 1,
            payment = False
        )
    except:
        pass
    return redirect('cart')

def cart(request):
    user = User.objects.get(email = request.session['email'])
    cart = Cart.objects.filter(user = user)
    subtotal = sum(i.total for i in cart)
    shipping = 3.00 if subtotal > 0 else 0.00
    grand_total = subtotal + shipping
    return render(request, 'cart.html', {'cart':cart, 'subtotal':subtotal, 'shipping':shipping, 'grand_total':grand_total})

def delete_cart(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk=pk)
    try:
        Cart.objects.filter(user=user, product=product).delete()
    except:
        pass
    return redirect('cart')

def Error(request):
    return render(request, 'Error.html')

def bestseller(request):
    return render(request, 'bestseller.html')

def cheackout(request):
    return render(request, 'cheackout.html')

def shop(request):
    product = Product.objects.all()
    return render(request, 'shop.html', {'product':product})
