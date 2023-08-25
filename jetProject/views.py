from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .connect import Logical  # Importing the class
from .dbcertconnect import LogicalDB

#cslcn=Logical()


def testgvs(request):
    logical_instance = Logical()  # Create an instance of the class
    res = logical_instance.get_list_gouv()
    #logical_instance = LogicalDB() 

    context = {
        'gouv_list': res,
    }
    
    return render(request, 'homepage.html', context) 


# tester l'existance d'un titre dans la table tfich 
def test_exist_in_tfich(request):
    #logical_instance = Logical()  # Create an instance of the class
   # res = logical_instance.get_list_gouv()
   if(request.method == 'POST'):
        # delete all files from folder 
        numtitre = request.POST.get('numtitre')
        gouvtitre = request.POST.get('gouvtitre')
        # Créer deux instances de deux classes qui sont connectées sur deux bases différentes 
        #classe : dbcertconnect
        logical_instance = LogicalDB() 
        # classe connect
        logical_instance2 = Logical()
        # tester l'existance dans la table tfich 
        response_data=logical_instance.GetTitreExiste(numtitre,gouvtitre,0,9)  

        # tester l'existance dans la tables titres dans la base de données de dged 
        res =logical_instance2.tester_ged_existance(response_data,numtitre,gouvtitre,0)
        # ça veut dire existe dans les deux tables 

        if(response_data =='1' and res == '1'):
              request.session['session_code_titre'] = numtitre
                  #response_data=logical_instance.GetTitreExiste(12457,9,0,9)
              context = {
                'response_data': response_data,      
              }

        # ça veut dire existe dans la tables tfich et non dans la table titres dans titres
        elif (response_data =='1' and res=='0'): 
             request.session['session_code_titre'] = numtitre
             context = {
                'response_data': '2'  # Assuming 'gouv_list' is the key you want to use in the template
              } 
        elif (response_data =='0' and res=='0'): 
              context = {
                'response_data': '0'  # Assuming 'gouv_list' is the key you want to use in the template
              } 
        return JsonResponse({'msg': context})

# import multiple files into database 


def testgvs3(request):
     if request.method =='POST' : 
            numtitre = request.session['session_code_titre']
            gouvtitre = request.POST.get('gouvtitre')
            doubtitre = request.POST.get('doubtitre')
           
            logical_instance = LogicalDB() 
            codetitre = logical_instance.Increment_num_titre()
            #codetitre =logical_instance.get_next_title_code()
            res = logical_instance.ajouter_titre(codetitre,gouvtitre,doubtitre,numtitre)
            print(res)
            if(res) : 
                return JsonResponse({'msg' : '1'})
            else : 
                return JsonResponse({'msg' : '0'})

     else:
            return JsonResponse({'msg': 'Invalid request method'})

def insert_record_at_pos(request): 
    ins = Logical()
    x = ins.insert_record_at_position(request)
    
    if(x =="1"):
        context = {
            "res" : "1"
        }
        return JsonResponse(context)
    else : 
        context = {
            "res" : "0"
        }
        return JsonResponse(context)
           
    #ires=cslcn.get_list_gouv()
    #return ires
def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'homepage.html')

def login(request):
    # return HttpResponse('about')
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, 'login.html')


def ChangePass(request):
    # return HttpResponse('about')
    return render(request, 'ChangePass.html')
def consulterSimple(request):
    return render(request, 'viewconsult.html')

def index(request):
    return render(request, 'index.html')

def consulter(request):
    # return HttpResponse('about')
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR) 
    return render(request, 'consultation.html')

def get_dash(request):
    logical_instance = Logical()  # Create an instance of the Logical class
    
    # Call the select_users function from the logical_instance
    selected_users = logical_instance.select_users()
    
    context = {
        'selected_users': selected_users
    }
    
    return render(request, 'dash.html', context)

def get_dashtitres(request):
    return render(request, 'dashtitres.html')

def get_statistiues(request):
    try:
        ins = Logical()
        result_list = ins.get_stat()

        # Other code related to your view

        context = {
            'result_list': result_list,
            # Other context variables
        }

        return render(request, 'stat.html', context)
    
    except Exception as e:
        print("Error:", e)
        return render(request, 'error.html')
def adduser(request):
    return render(request, 'adduser.html')

def get_first(request):
    return render(request, 'first.html')
def admin(request):
    return render(request, 'admin.html')
def test(request):
    return render(request, 'test.html')
def exist(request):
    return render(request, 'exist.html')


import os
import base64
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from PIL import Image

def export_and_show_file(request):
    # Replace 'D:\tempd\s15.tiff' with the desired file path where the file should be saved
    file_path_tiff = 'D:\\tempd\\s15.tiff'
    file_path_png = 'D:\\tempd\\s15.png'  # Path for the converted .png file

    with connection.cursor() as cursor:
        # Execute the lo_export query
        cursor.execute("SELECT lo_export(docs, %s) FROM images WHERE docs = 25057;", [file_path_tiff])

    # Check if the file was successfully exported
    if os.path.exists(file_path_tiff):
        print("Before Conversion: ", file_path_tiff)

        # Convert the .tiff image to .png format
        img = Image.open(file_path_tiff)
        img.save(file_path_png, 'PNG')
        img.close()
        print("After Conversion: ", file_path_png)


        # Open the converted .png file in binary read mode
        with open(file_path_png, 'rb') as file:
            # Read the file data
            file_data = file.read()

        # Delete the .tiff and .png files after reading the data to avoid filling up the server disk
        os.remove(file_path_tiff)
        os.remove(file_path_png)

        # Convert binary data to base64-encoded string
        file_data_base64 = base64.b64encode(file_data).decode('utf-8')

        # Render the HTML template and pass the base64-encoded image data as context
        return render(request, 'homepage.html', {'file_data_base64': file_data_base64})
    else:
        return render(request, 'file_not_found.html')



def GetTitreExiste(self, request):
    numtitre = request.POST.get('numtitre')
    gouvtitre = request.POST.get('gouvtitre', "0")  # Set default value to "0" if 'gouvtitre' is not provided
    doubtitre = request.POST.get('doubtitre', "0")  # Set default value to "0" if 'doubtitre' is not provided
    dreg = request.POST.get('dreg')

    if not gouvtitre:
        gouvtitre = 0
    if not doubtitre:
        doubtitre = 0

    xquery = ('''SELECT numtitre, gouvtitre, doubtitre, dreg FROM tfich WHERE numtitre = %s AND gouvtitre = %s AND doubtitre = %s AND dreg = %s AND typfiche = 1''')
    curs = self.conn.cursor()
    curs.execute(xquery, [numtitre, gouvtitre, doubtitre, dreg])
    rows = curs.fetchall()

    if len(rows) > 0:
        for row in rows:
            iquery = ('''SELECT * FROM tfich WHERE numtitre = %s AND gouvtitre = %s AND doubtitre = %s AND dreg = %s AND typfiche = 3''')
            cur1 = self.conn.cursor()
            cur1.execute(iquery, [row[0], row[1], row[2], row[3]])
            irows = cur1.fetchall()
            # self.conn1.close()
            if len(irows) > 0:
                return "2"
            else:
                return "1"
    else:
        return "0"



def data_insert():

    logical_instance = Logical()  # Create an instance of the class
        #response_data =logical_instance.insert_titre(request)  # Call the insert_titre function
        
    response_data=LogicalDB.tester_ged_existance()
    
    return JsonResponse(response_data)
  
# Function that import multiple files to the specific title 

def test_import(request):
    logical_instance = Logical()
    response_message = logical_instance.import_files_with_codetitre(request)
    response_data = {'message': response_message}
    print(response_data)
    return JsonResponse(response_data)




def tester_titre_existance(request):

    if(request.method == 'POST') : 

        numtitre =  int(request.POST.get('numtitre'))
        gouvtitre = int(request.POST.get('gouvtitre', "0") ) # Set default value to "0" if 'gouvtitre' is not provided
        doubtitre = int(request.POST.get('doubtitre', "0") ) # Set default value to "0" if 'doubtitre' is not provided
        # créer une instance de la clase connect qui est liée à la base de données de ged 
        logical_instance = Logical() 
        # Tester l'existance dans la table de titres sans Ged
        response_data =  logical_instance.tester_ged_existance(numtitre,gouvtitre,doubtitre)
        return JsonResponse({'msg' : response_data})
    else:
        return JsonResponse({'msg':'Type de requete invalide'})

# got to the folder and display all the images 
def display_images_from_tempd(request):
    ins = Logical()
    images,numlen = ins.display_images(request)

    response_data = {'images': images, 'count': numlen}
    print('Numlen = ',numlen)
    return JsonResponse(response_data)



# tester le téléchargement des images dans le dossier tempd
#def del_All(request) : 
  #  ins = Logical()
  #  print(ins.delete_all_files())
   # if(ins.delete_all_files()) : 
   #    return JsonResponse({'message' : 'All deleted with success'})
    #else : 
     #  return JsonResponse({'message' : 'Not deleted'}) 
        
def find_dell(request):
    if(request.method == 'POST') : 
        prefix_value = request.POST.get('prefix_value')
        ins = Logical()
        doc_file = ins.find_to_delete(request,prefix_value)
        return JsonResponse({'res' : doc_file})

def get_count_titresimages(request) : 
    ins = Logical()
    return JsonResponse({'num' : ins.get_count(request) })




def delete_from_tuser(request, user_id):
    try:
        if request.method == 'DELETE':
            ins = Logical()
            print("Received user_id:", user_id)  # Add this line to print the received user_id
            result = ins.delete_users_by_id(user_id)  # Call delete_users_by_id with a single user ID
            print(result)
            if result:
                return JsonResponse({'res': '1'}, status=200)
            else:
                return JsonResponse({'res': '0'}, status=500)
        else:
            print('It\'s not a DELETE request')
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'res': '0'}, status=500)







def add_emp(request):
    try:
        if request.method == 'POST':
            ins = Logical()
            username = request.POST.get('username')
            password = request.POST.get('password')
            tipe = int(request.POST.get('type'))
            status = int(request.POST.get('status'))
            address = request.POST.get('address')
            etat = int(request.POST.get('etat'))
            role = int(request.POST.get('role'))

            result = ins.add_new_user(username, password, tipe, status, address, etat, role)

            if result:
                return JsonResponse({'res': '1'}, status=200)
            else:
                return JsonResponse({'res': '0'}, status=500)
        else:
            print('It\'s not a POST request')
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'res': '0'}, status=500)

# get One single user  



def get_user_details(request):
    try:
        ins = Logical()

        idemp = request.GET.get('idemp')  # Get the idemp from the GET request parameter
        print('Idemp =  ',idemp)
        user_data = ins.get_user_by_idemp(idemp)

        if user_data:
            return JsonResponse({'res': '1', 'user_data': user_data})
        else:
            return JsonResponse({'res': '0', 'error': 'User not found'}, status=404)

    except Exception as e:
        print("Error:", e)
        return JsonResponse({'res': '0', 'error': 'An error occurred'}, status=500)

# Update user By idemp 

def update_user_by_idemp(request):
    if request.method == 'POST':
        try:
            idemp = request.POST.get('idemp')
            username = request.POST.get('username1')
            password = request.POST.get('password1')
            tipe = request.POST.get('type1')
            status = request.POST.get('status1')
            address = request.POST.get('address1')
            etat = request.POST.get('etat1')
            role = request.POST.get('role1')

            ins = Logical()  # Create an instance of the Logical class
            result = ins.update_user_by_idemp(idemp, username, password, tipe, status, address, etat, role)

            if result:
                return JsonResponse({'res': '1'}, status=200)
            else:
                return JsonResponse({'res': '0'}, status=500)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'res': '0'}, status=500)
    else:
        print('It\'s not a POST request')
        return JsonResponse({'res': '0'}, status=500)




def login_emp(request):
    if request.method == 'POST':
        username = request.POST.get('userauth')
        password = request.POST.get('passwd')
      

        ins = Logical()  # Create an instance of the Logical class
        user_data = ins.get_user_by_username_password(username, password)

        if user_data:
            # Log the user in and set session or cookies
            request.session['user_id'] = user_data[0]
            request.session['username'] = user_data[1]
            
            return JsonResponse({'res': '1'})  # User found
        else:
            return JsonResponse({'res': '0'})  # User not found

    return render(request, 'login.html')

def change_password_view(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            old_password = request.POST.get('old')
            new_password = request.POST.get('new')
            user_id = request.session.get('user_id')

            ins = Logical()  # Create an instance of the Logical class
            result = ins.change_password(old_password, new_password, user_id)

            if result:
                return JsonResponse({'res': '1'}, status=200)
            else:
                return JsonResponse({'res': '0'}, status=200)
        else:
            return JsonResponse({'res': '0'}, status=500)
    else:
        return JsonResponse({'res': '0'}, status=401)  # Unauthorized response




# Import the Logical class

def display_images_view(request):
    # Create an instance of the Logical class
    ins = Logical()
    print(request.POST)
    posFrom = request.POST.get('posFrom')
    posTo = request.POST.get('posTo')
    print('posFrom = ',posFrom)
    print('posTo = ',posTo)
    # Call the display_images_paginations method
    images, count, countImage = ins.display_images_paginations(request, posFrom,posTo)
    # Create a response data dictionary
    response_data = {
        'images': images,
        'count': count,
        'countImage' : countImage
    }

    # Return the response as JSON
    return JsonResponse(response_data)


from PIL import Image
import os
import base64

def tiff_to_png(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            img.save(output_path, "PNG")
        
        return True
    except Exception as e:
        print(f"Error converting TIFF to PNG: {e}")
        return False

def display_images_from_folder(request):
    folder_path = 'C:/Users/Amir/Desktop/tiffFiles'  # Replace with your folder path
    
    try:
        images_data = []
        

        # Get a list of all files in the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        imgs = files
        for file_name in files:
            # Check if the file is a TIFF file
            if file_name.lower().endswith('.tiff') or file_name.lower().endswith('.tif'):
                # Convert TIFF to PNG and save it to a temporary file
                tiff_path = os.path.join(folder_path, file_name)
                png_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + '.png')
                
                if tiff_to_png(tiff_path, png_path):
                    # Read the PNG file and convert it to base64
                    with open(png_path, 'rb') as file:
                        image_data = base64.b64encode(file.read()).decode('utf-8')
                        images_data.append(image_data)
                    
                    # Remove the temporary PNG file
                    os.remove(png_path)

        response_data = {
            'images': images_data,
            'imgs' : imgs
        }
        print(imgs)
        return JsonResponse(response_data)
    except Exception as e:
        # Handle any exceptions or errors here
        error_message = str(e)
        response_data = {
            'error': error_message,
        }
        return JsonResponse(response_data, status=500)









