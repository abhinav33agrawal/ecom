from django.shortcuts import render,redirect
from shop import models
from django.contrib.auth.hashers import make_password,check_password
from shop.auth import auth_middleware

# from shop import middleware
# Create your views here.
def index(request):
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
            # request.session.get('cart').clear()
        products = models.Product.get_all_products()
        categories = models.Category.get_all_categories()
        if request.GET.get('category'):
            products = models.Product.get_all_prod_byId(request.GET['category'])
        return render(request,'index.html',{'prods':products,'cats':categories})
    else:

        return i(request)
        

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        data = {'firstname':firstname,'lastname':lastname,'email':email,'phone':phone}
        customer = models.Customer(firstname=firstname,lastname=lastname,email=email,phone=phone,password=password)

        error_mess = None
        if not firstname:
            error_mess = 'Please fill first name'
        elif not lastname:
            error_mess = 'Please fill last name'
        elif not email:
            error_mess = 'Please fill email'
        elif customer.isExist():
            error_mess = 'Email Already Exists'
        elif not password:
            error_mess = 'Please enter password'
        elif not phone:
            erro_mess = 'Please enter phone no.'
        if error_mess:
            return render(request,'signup.html',{'error':error_mess,'data':data})
        
        customer.password = make_password(password)
        customer.register()

        return redirect('/')

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email = request.POST['email']
        password = request.POST['password']
    
        error_message = None
        if not email:
            error_message = 'Please enter email Address'
            return render(request,'login.html',{'error':error_message})
        elif not password:
            error_message = 'Please enter password'
            return render(request,'login.html',{'error':error_message,'email':email})

        


        customer = models.Customer.get_by_email(email=email)
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                request.session['customer'] = customer.id 
                return redirect("/")
            else:
                error_message = 'Invalid Email or password'
                return render(request,'login.html',{'error':error_message,'email':email})  
        else:
            error_message = 'Invalid Email or Password'
            return render(request,'login.html',{'error':error_message,'email':email})  
def logout(request):
    request.session.clear()
    return redirect('login')

def cart(request):
    cart = request.session.get('cart')
    ids = list(cart.keys())
    product = models.Product.get_by_prodId(ids)
    return render(request,'cart.html',{'products':product})

def place_order(request):
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    customer = request.session.get('customer')
    cart = request.session.get('cart')
    products = models.Product.get_by_prodId(list(cart.keys()))
    for product in products:
        order = models.Order(phone= phone,product=product,customer=models.Customer(id=customer),address=address,quantity=cart.get(str(product.id)))
        order.save()
        
    request.session['cart'] = {}

    return redirect('cart')


def orders(request):
    customer = request.session.get('customer')
    order = models.Order.get_by_custoId(customer)
    return render(request,'orders.html',{'orders':order})

@auth_middleware
def i(request):
    remove = request.POST.get('remove')   

    product = request.POST.get('product')
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product)
        if quantity:
            if remove:
                if quantity==1:
                    cart.pop(product)
                else:
                    cart[product] = quantity-1
            else:
                cart[product] = quantity+1
        else:
            cart[ product] = 1
    else:
        cart = {}
        cart[product] = 1
    request.session['cart'] = cart
    return redirect('/')
    

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'GET':
        return render(request,'contact.html')
    else:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        desc = request.POST.get('desc')

        Data = models.ContactUs(name=name,phone=phone,email=email,problem=desc)
        Data.save()
        return redirect('/')

