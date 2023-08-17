import psycopg2
import sys
import logging
#import datetime
import os
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from PIL import Image
import base64  # Add this import


class Logical :    
    def __init__(self):
        try:
            self.conn = psycopg2.connect( user = "postgres",
            password = "amir169114",
            host = "localhost",
            port = "5432",
            database = "immo")                            
            self.conn.set_client_encoding('WIN1256')  
                  
        except psycopg2.DatabaseError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened successfully.')

    def run_command(self,query,params):

        try:
            with self.conn.cursor() as cur:
                cur.execute(query,params)
                self.conn.commit()
                affected = f"{cur.rowcount}"
                cur.close()
                #return affected
        except psycopg2.DatabaseError as e:
            return jsonify({"status" : "-2"})
        finally:
            if self.conn:
                #self.conn.close()
                logging.info('Database connection closed.')
                return jsonify({"status" : affected})
            
    def getdictres(self,rows):
        result = []
        for row in rows:               
            x={}
            for i in range(len(row)):
                x[i] = row[i]
                
            result.append(x)
            
        return result



    # test
    def hellowd(self):
        
        return 'welcome amira'

    def get_list_gouv(self):
        Sql = '''
            select codgouv, libgouv, dr from tgouv  order by codgouv
        '''
        curs = self.conn.cursor()
        curs.execute(Sql)
        resultat = curs.fetchall()
        res = self.getdictres(resultat)
        return res


    # insérer les titres qui existent dans la base de données 

    def insert_titre(self, request):
        numtitre = request.POST.get('numtitre')
        codgouv = request.POST.get('codgouv')
        doubtitre = request.POST.get('doubtitre')
        nbpage = request.POST.get('nbpage')

        logical_instance = Logical()  # Create an instance of the class
        titre_exists = logical_instance.GetTitreExiste(numtitre, gouvtitre, doubtitre, dreg)
        
        if titre_exists == "0":
            # Titre doesn't exist, insert it
            with self.conn.cursor() as cursor:
                insert_query = """
                INSERT INTO tfich (numtitre, gouvtitre, doubtitre, dreg, typfiche)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, [numtitre, gouvtitre, doubtitre, dreg, 1])  # Assuming typfiche is 1 for insertion
                
            self.conn.commit()  # Commit the transaction
            return JsonResponse({'message': 'Data inserted successfully'})
        elif titre_exists == "1":
            return JsonResponse({'message': 'Titre exists with typfiche=1'})
        elif titre_exists == "2":
            return JsonResponse({'message': 'Titre exists with typfiche=3'})

    # Add a new title

    def ajouter_titre(self,numtitre,gouvtitre,doubtitre,nbpage):
            insert_query = '''INSERT INTO titres (numtitre, gouvtitre, doubtitre, nbpage) VALUES (%s, %s, %s, %s)'''
            print(numtitre,gouvtitre,doubtitre,nbpage)
            cursor = self.conn.cursor()
            cursor.execute(insert_query, [numtitre, gouvtitre, doubtitre, nbpage])
            self.conn.commit() 
            return "titre inserted with success"

    # Tester l'existance d'un titre dans la table titres de la base de GED

    def tester_ged_existance(self,exist,numtitre,gouvtitre,doubtitre) : 
        # si le titres déja existe dans la base en ligne la dbfoncier qui contient la table tfich  
        if(exist =='1'):
            check_query = "SELECT COUNT(*) FROM titres WHERE numtitre = %s AND gouvtitre = %s AND doubtitre = %s"
            cursor = self.conn.cursor()
            cursor.execute(check_query, [numtitre, gouvtitre, doubtitre])
            title_exists = cursor.fetchone()[0] > 0
            if title_exists:
                return "1"
            else:
                return "0"
        # ligne n'existe pas dans la table enligne
        else : 
            return "0"
    # import multiple files into database 

    def upload_files_from_database(self,codetitre):
        folder_path = 'D:/tempd/'
        test = False

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT codetitre, numpage, doc FROM titresimages WHERE codetitre = %s", [codetitre])
                files_to_export = cursor.fetchall()

                if len(files_to_export) == 0:
                    return True
                
                for (codetitre, numpage, oid_value) in files_to_export:
                    file_name = f"{str(numpage)}_{str(codetitre)}.tiff"
                    new_file_path = os.path.join(folder_path, file_name)

                    lo_export_query = f"SELECT lo_export({oid_value}, '{new_file_path}')"
                    cursor.execute(lo_export_query)

                    if os.path.exists(new_file_path):
                        test = True
                    else:
                        test = False
                        break  # Stop processing if export fails

        except Exception as e:
            print(e)
            test = False

        return test




  # ... (other methods)

    @transaction.atomic
    def import_files_with_codetitre(self, request):
        if request.method == 'POST' and request.FILES:
            self.delete_all_files()
            print("Files deleted with success")
            uploaded_files = request.FILES.getlist('files')

            if 'session_code_titre' not in request.session:
                return HttpResponse("Session variable session_code_titre is not set")

            codetitre = request.session['session_code_titre']

            # Check if images exist for the given codetitre
            existing_images_count = self.get_count(request)  # Replace with your count retrieval function

            with self.conn.cursor() as cursor3:
    # Get the current maximum numpage for the given codetitre
                cursor3.execute("SELECT MAX(numpage) FROM titresimages WHERE codetitre = %s", [codetitre])
                max_numpage = cursor3.fetchone()[0]

                if max_numpage is None:
                    max_numpage = 0

                for idx, uploaded_file in enumerate(uploaded_files, start=max_numpage + 1):
                    # Generate a unique number for each uploaded file
                    unique_num = self.get_unique_number(cursor3)

                    # Create the new filename using unique number and original file name
                    file_name = f"{unique_num}_{uploaded_file.name}"
                    file_path = os.path.join('D:/tempd/', file_name)

                    with open(file_path, 'wb') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)

                    try:
                        cursor3.execute("""
                            INSERT INTO titresimages (codetitre, doc, numpage)
                            VALUES (%s, lo_import(%s), %s)
                        """, [codetitre, file_path, idx])

                        self.conn.commit()

                    except Exception as e:
                        print(e)
                        return '0'

                return '1'

        return '0'

# ... (imports and class definition)

# ... (other imports and class definition)

    def insert_record_at_position(self, request):
        if request.method == 'POST' and request.FILES:
            if 'session_code_titre' not in request.session:
                return HttpResponse("Session variable session_code_titre is not set")

            codetitre = request.session['session_code_titre']
            desired_position = int(request.POST['desired_position'])  # Extract desired_position from the POST request
            uploaded_file = request.FILES['files']  # Get the uploaded file
            existing_images_count = self.get_count(request)  # Replace with your count retrieval function

            with self.conn.cursor() as cursor5:
                cursor5.execute("SELECT MAX(numpage) FROM titresimages WHERE codetitre = %s", [codetitre])
                max_numpage = cursor5.fetchone()[0]

                if max_numpage is None:
                    max_numpage = 0

                if desired_position > max_numpage:
                    new_numpage = desired_position
                else:
                    cursor5.execute("UPDATE titresimages SET numpage = numpage + 1 WHERE codetitre = %s AND numpage >= %s", [codetitre, desired_position])
                    new_numpage = desired_position

                file_name = uploaded_file.name
                file_path = os.path.join('D:/tempd/', file_name)

                try:
                    # ... (other code for file write)

                    with open(file_path, 'wb') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)

                    # Insert record into the database
                    cursor5.execute("""
                        INSERT INTO titresimages (codetitre, doc, numpage)
                        VALUES (%s, lo_import(%s), %s)
                    """, [codetitre, file_path, new_numpage])

                    self.conn.commit()
                    self.display_images(request)
                    print('Record inserted successfully')

                except Exception as e:
                    print('Exception was occurred')
                    print(e)
                    return '0'
                
                return '1'
        print('Not inserted')
        return '0'








    
    def get_unique_number(self, cursor):
        # Get the current length of the titresimages table
        cursor.execute("SELECT COUNT(*) FROM titresimages;")
        table_length = cursor.fetchone()[0]

        # Generate a unique number based on table length and current index
        unique_num = table_length + 1
        return unique_num
        
    def display_images(self, request):
        folder_path = 'D:/tempd/'  # Path to the folder containing images
        images = []
        codetitre = request.session['session_code_titre']

        if self.delete_all_files():  # Execute delete function and check its result
            if self.upload_files_from_database(codetitre):
                image_files = [filename for filename in os.listdir(folder_path)]

                print("codetitre =", codetitre)
                for image_file in image_files:
                    file_path_tiff = os.path.join(folder_path, image_file)
                    file_path_png = os.path.splitext(file_path_tiff)[0] + '.png'

                    with self.conn.cursor() as cursor2:
                        # Execute the lo_export query
                        cursor2.execute("SELECT lo_export(doc, %s) FROM titresimages WHERE codetitre = %s;", [file_path_tiff, codetitre])

                    if os.path.exists(file_path_tiff):
                        print("Before Conversion:", file_path_tiff)

                        # Convert the .tiff image to .png format
                        img = Image.open(file_path_tiff)
                        img.save(file_path_png, 'PNG')
                        img.close()
                        print("After Conversion:", file_path_png)

                        # Open the converted .png file in binary read mode
                        with open(file_path_png, 'rb') as file:
                            # Read the file data
                            file_data = file.read()

                        # Delete the .tiff and .png files after reading the data to avoid filling up the server disk
                        os.remove(file_path_tiff)
                        #os.remove(file_path_png)

                        # Convert binary data to base64-encoded string
                        file_data_base64 = base64.b64encode(file_data).decode('utf-8')
                        images.append(file_data_base64)
                        print('images')
        else:
            images = []

        return images



    # delete all files from tempd folder  

    def delete_all_files(self):
        folder_path = 'D:/tempd/'
        test = False 
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            test = True
        except Exception as e:
            print(e)
            test = False
        return test

    def find_to_delete(self,request,prefix_value):
        folder_path = 'D:/tempd/'
        code_titre = int(request.session['session_code_titre'])
        print(code_titre)
        try:
            file_names = [os.path.splitext(f[2:])[0] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.startswith(str(prefix_value) + '_')]
            if file_names:
                file_name = file_names[0]  # Get the first file_name
                print(file_name)
                with self.conn.cursor() as cursor2:
                    # Delete the row based on 'code_titre' and 'file_name'
                    cursor2.execute("DELETE FROM titresimages WHERE codetitre = %s AND doc = %s;", [code_titre, int(file_name)])
                    self.conn.commit()  # Commit the transaction

                return True  # Return True to indicate successful deletion
            else:
                return False  # Return False to indicate no file found
        except Exception as e:
            print("Error:", e)
            return False  # Return False to indicate an error




    def get_count(self, request):
        code_titre = int(request.session['session_code_titre'])   
        try:
            with self.conn.cursor() as cursorN:
                # Execute a SELECT query to get the count of images
                cursorN.execute("SELECT COUNT(*) FROM titresimages WHERE codetitre = %s;", [code_titre])
                images_count = cursorN.fetchone()[0]
            
            if images_count:
                return images_count  # Return the count of images
            else:
                return 0  # Return 0 to indicate no file found
        except Exception as e:
            print("Error:", e)
            return -1  # Return -1 to indicate an error





    # Crud for Users
    def select_users(self):
        selected_users = []  # List to store selected users
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users_tuser;")
                selected_users = cursor.fetchall()  # Fetch all rows
            
            return selected_users  # Return the list of selected user data
        except Exception as e:
            print("Error:", e)  
            return []  # Return an empty list in case of an error


    def delete_users_by_id(self, user_id):
        test = False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM users_tuser WHERE idemp = %s;", [int(user_id)])
                self.conn.commit()
                test = True  # Set test to True to indicate successful deletion
                
            return test  # Return True if successful, otherwise False
        except Exception as e:
            print("Error:", e)
            return test  # Return False in case of an error
            



    def add_new_emp(self,username,password,tip,status,address,etat,role):
            import hashlib
            try:
                # Hash the password
                strpwd = password + str(username)
                hashed_password = hashlib.md5(strpwd.encode()).hexdigest()

                # Insert the user data using a cursor
                with self.conn.cursor() as cursor:
                    cursor.execute("INSERT INTO users_tuser (userauth,passwd, categorie,active, add_ip,etat,role) VALUES (%s, %s, %s, %s, %s, %s);",
                                [username, password, tip, status,address, etat,role])
                    self.conn.commit()

                return True
            except Exception as e:
                print("Error:", e)
                return False