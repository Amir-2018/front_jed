from django.http import JsonResponse
from django.core import serializers
import hashlib
from .models import TUser
from django.shortcuts import  redirect, render
from django.core.paginator import Paginator


# display all users

def user_list(request):
    print('test')
    
def get_list_users(request):
    users = TUser.objects.all()
    # Set the number of users per page
    paginator = Paginator(users, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'users':users
    }
    return render(request, 'users/user_list.html', context)

# Insert users

def insert_user(request):
    # Check if the request is a POST request
    if request.method == 'POST':
            # Extract the user data from the request's POST parameters
            idemp = TUser.objects.count() + 10   
            # Increment the user count by 1 to get the new idemp value
            userauth = request.POST.get('userauth')
            passwd = request.POST.get('passwd')
            categorie = request.POST.get('categorie')
            active = request.POST.get('active')
            adr_ip = request.POST.get('adr_ip')
            etat = request.POST.get('etat')
            role = request.POST.get('role')

            if TUser.objects.filter(userauth=userauth).exists():
                response_data = {'message': 'Uerauth already in use'}
                return JsonResponse(response_data)
            else : 
            # Create a new TUser object
                user = TUser(
                    idemp=idemp,
                    userauth=userauth,
                    passwd='',
                    categorie=categorie,
                    active=active,
                    adr_ip=adr_ip,
                    etat=etat,
                    role = role
                )
                # Hash the password using MD5
                strpwd = passwd + str(idemp)
                hashed_password = hashlib.md5(strpwd.encode()).hexdigest()
                
                # Set the hashed password
                user.passwd = hashed_password
                print(idemp)
                # Save the user to the database
                user.save()
            
                # Return a JSON response indicating successful user insertion
                response_data = {'message': 'User inserted successfully'}
                return redirect('/users/get_users/')
        
                # Return an error JSON response if the request is not a POST request
                response_data = {'error': 'Invalid request method'}
                return JsonResponse(response_data, status=400)

    
def login_user(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('userauth')
        reqpwd = request.POST.get('passwd')
        
        try:
            user = TUser.objects.get(userauth=username)
            # effacer espace au début et à la  fin de la chaine 
            passwddb = user.passwd.strip()
            iduser = user.idemp
            strpwd = reqpwd + str(iduser)
            passwd = hashlib.md5(strpwd.encode()).hexdigest().strip()
            if passwd == passwddb:
                request.session['username'] = username
                if(user.role==1):
                    return redirect('/adminUser')
                else : 
                    return redirect('/smp')

            else:
                # error = 'معطيات غير متطابقة مع قاعدة البيانات الرجاء التثبت'
                error = "check your credentials please"
                return redirect('/login',error)
        except TUser.DoesNotExist:
            error = "check your credentials please"
            return redirect('/login',error)
            
    return render(request, 'login.html', {'error': error})
    

def delete_user(request, user_id):
    # Check if the request is a GET request
    if request.method == 'GET':
        try:
            # Get the user by their ID from the TUser table
            user = TUser.objects.get(idemp=user_id)
            
            # Delete the user
            user.delete()
            
            msg_success = "User deleted successfully"
            return redirect('/users/get_users/')
            
        except TUser.DoesNotExist:
            error = "User could not be deleted"
            return JsonResponse({'error': error})


def update_user(request, user_id):
    # Check if the request is a POST request
    if request.method == 'POST':
        try:
            # Get the user by their ID from the TUser table
            user = TUser.objects.get(idemp=user_id)
            
            # Update the user attributes with the provided parameters
            user.userauth = request.POST.get('userauth')
            user.passwd = request.POST.get('passwd')
            user.categorie = request.POST.get('categorie')
            user.active = request.POST.get('active')
            user.adr_ip = request.POST.get('adr_ip')
            user.etat = request.POST.get('etat')
            
            # Save the updated user object
            user.save()
            
            msg_success = "User updated successfully"
            return JsonResponse({'success': msg_success})        
        except TUser.DoesNotExist:
            error = "User not found"
            return JsonResponse({'error': error})

import hashlib

# get user with id 

def get_user_by_idemp(request,idemp):
    if request =='GET':
        return HttpResponse("Get request")
    else : 
        return HttpResponse("other request")
    #user = TUser.objects.get(idemp=user_id)
    #get_users_url = reverse('get_users')  # Replace 'get_users' with the actual URL pattern or view name
    #return redirect(users/get_users, user_idemp=user.idemp)


def changePass(request):
    error = None
    if request.method == 'POST':
        username = request.session.get('username')
        print(username)
        reqpwd = request.POST.get('old')
        newpwd = request.POST.get('new')
        
        try:
            user = TUser.objects.get(userauth=username)
            # Get the old password
            passwddb = user.passwd.strip()
            iduser = user.idemp
            strpwd = reqpwd + str(iduser)
            hashpasswd = hashlib.md5(strpwd.encode()).hexdigest().strip()
            print(passwddb)
            print(hashpasswd)
            if hashpasswd == passwddb:
                # Update the password with the new password
                strnewpwd = newpwd + str(iduser)
                newpasswd = hashlib.md5(strnewpwd.encode()).hexdigest().strip()
                user.passwd = newpasswd
                user.save()
                response_data = {'message': 'Password updated successfully'}
                return JsonResponse(response_data)
            else:
                error = "Check your credentials, please"
                return JsonResponse({'error': error})
        except TUser.DoesNotExist:
            error = "Please try again"
            # error = 'الرجاء إعادة المحاولة'
            # try again, please
            return JsonResponse({'error': error})
            
    return render(request, 'login.html', {'error': error})
from django.shortcuts import render, get_object_or_404

def update_user(request,user_id):
    user = get_object_or_404(TUser, idemp=user_id)

    # Pass the 'user' object to the 'update.html' template
    return render(request, 'users/update.html', {'user': user})




def update_user_crud(request, user_id):
    user = get_object_or_404(TUser, idemp=user_id)

    if request.method == 'POST':
        # Update the user's fields with the form data
        user.userauth = request.POST.get('userauth')
        user.passwd = request.POST.get('passwd')
        user.categorie = request.POST.get('categorie')
        user.active = request.POST.get('active')
        user.adr_ip = request.POST.get('adr_ip')
        user.etat = request.POST.get('etat')

        # Save the updated user to the database
        user.save()

        # Redirect to a success page or any other appropriate view
        return redirect('/users/get_users')  # You can replace 'user_updated' with the name of your success page URL pattern

    # If it's a GET request, render the 'users/update.html' template with the user object
    return render(request, 'users/update.html', {'user': user})
