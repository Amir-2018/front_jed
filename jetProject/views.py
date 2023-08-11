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

        if(res == '1'):
              request.session['session_code_titre'] = numtitre
                  #response_data=logical_instance.GetTitreExiste(12457,9,0,9)
              context = {
                'response_data': response_data,      
              }

        # ça veut dire existe dans la tables tfich et non dans la table titres dans titres
        else : 
              context = {
                'response_data': '0'  # Assuming 'gouv_list' is the key you want to use in the template
              } 
        return JsonResponse({'msg': context})

# import multiple files into database 

def testgvs3(request):
     if request.method =='POST' : 
            
            gouvtitre = request.POST.get('gouvtitre')
            doubtitre = request.POST.get('doubtitre')
            nbpage = request.POST.get('nbpage')  # You need to provide 'dreg' in your POST data
            logical_instance = LogicalDB() 
            numtitre =logical_instance.Increment_num_titre()
            print(numtitre)
            res = logical_instance.ajouter_titre(numtitre,gouvtitre,doubtitre,nbpage)
            print(res)
            if(res) : 
                return JsonResponse({'msg' : '1'})
            else : 
                return JsonResponse({'msg' : '0'})

     else:
            return JsonResponse({'msg': 'Invalid request method'})

           

    #ires=cslcn.get_list_gouv()
    #return ires
def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'homepage.html')

def login(request):
    # return HttpResponse('about')
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
    images = ins.display_images(request)
    response_data = {'images': images}
    return JsonResponse(response_data)


# tester le téléchargement des images dans le dossier tempd
#def del_All(request) : 
  #  ins = Logical()
  #  print(ins.delete_all_files())
   # if(ins.delete_all_files()) : 
   #    return JsonResponse({'message' : 'All deleted with success'})
    #else : 
     #  return JsonResponse({'message' : 'Not deleted'}) 
        



