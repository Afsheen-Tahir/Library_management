
from django.shortcuts import render,redirect
from management.models import Management,Cart;
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Management, pk=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def view_cart(request):
    if request.user.is_authenticated:
        items = Cart.objects.filter(user=request.user)
        total = sum(item.total_price() for item in items)
        message=" "
    else:
        items = []
        total = 0
        message="Log In required to see Books"

    return render(request, 'Cart/cart.html', {'items': items, 'total': total,'message':message})



@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, pk=item_id, user=request.user)
    item.delete()
    return redirect('cart')

def books(request):
   query = ''
   message = '' 
   filter=''
   if request.method == 'GET':
        
        books = Management.objects.all()
        query = request.GET.get('query', '')
        filter=request.GET.get('books','')
        if query:
            books=books.filter(Booktitle__icontains=query)
         
        if filter=='Rating':
           books = books.order_by('BookRating')
        elif filter=='New to Old':
           books = books.order_by('-id')
        elif filter=='Old to New':
           books = books.order_by('id')
          
        message = "Book not found" if query and not books.exists() else ''
            
        
   datasend={
                'data':books,
                'message': message ,
                'filter':filter

            }
       
   return render(request,'Books/index.html',datasend)
def Main(request):
    data=Management.objects.all().order_by('id')[:4]
    dataSend={
       'dataget':data
    }
    
    return render(request, 'UserView/userview.html',dataSend)

def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already registered.")
            return redirect('signin')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signin')


        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        auth_login(request, user) 
        
        return redirect('Main') 
    return render(request, 'SignIn/index.html')
def Login(request):
    if request.method == 'POST':
        name = request.POST.get('user_login')
        password = request.POST.get('user_pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            auth_login(request, user)
            
            return redirect('cart')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'Login/index.html')

@login_required
def logout(request):
    auth_logout(request)
    
    return redirect('login')

def Bookdetail(request,bookid):
    book=Management.objects.get(pk=bookid)
   
    return render(request,'bookdetail/index.html', {'book': book})
