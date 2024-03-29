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


    def ajouter_titre(self,numtitre,gouvtitre,doubtitre):
            test_tfich_exist = self.GetTitreExiste(numtitre, gouvtitre, 0, 9)
            if(test_tfich_exist =='1') : 
                print('Existe')
            else : 
                print('Not existe')
           # insert_query = '''INSERT INTO titres (codetitre,numtitre, gouvtitre, doubtitre) VALUES (%s, %s, %s,%s)'''
           # print(numtitre,gouvtitre,doubtitre,nbpage)
            #cursor = self.conn.cursor()
            #print('num = ',get_next_title_code)
            #cursor.execute(insert_query, [get_next_title_code,numtitre, gouvtitre, doubtitre])
            #self.conn.commit() 
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

    def upload_files_from_database(self, codetitre):
        folder_path = 'D:/tempd/'
        test = False

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT codetitre, numpage, doc FROM titresimages WHERE codetitre = %s ORDER BY numpage ASC LIMIT 10;", [codetitre])
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



    def upload_files_from_database_pages(self, codetitre, posFrom, posTo):
        folder_path = 'D:/tempd/'
        test = False
        files_exported_count = 0  # Initialiser le compteur des fichiers exportés

        try:
            with self.conn.cursor() as cursor:
                # Sélectionnez les images en fonction de la colonne numpage
                cursor.execute("SELECT codetitre, numpage, doc FROM titresimages WHERE codetitre = %s AND numpage BETWEEN %s AND %s", [codetitre, posFrom, posTo])
                files_to_export = cursor.fetchall()

                if len(files_to_export) == 0:
                    return (test, files_exported_count)  # Retourner les deux valeurs

                # Triez les fichiers localement en fonction de la dernière colonne (numpage)
                files_to_export.sort(key=lambda x: x[-1])  # Triez par la dernière colonne (numpage)

                for (codetitre, numpage, oid_value) in files_to_export:
                    file_name = f"{str(numpage)}_{str(codetitre)}.tiff"
                    new_file_path = os.path.join(folder_path, file_name)

                    lo_export_query = f"SELECT lo_export({oid_value}, '{new_file_path}')"
                    cursor.execute(lo_export_query)

                    if os.path.exists(new_file_path):
                        test = True
                        files_exported_count += 1  # Incrémenter le compteur des fichiers exportés
                    else:
                        test = False
                        break  # Arrêter le traitement en cas d'échec de l'export

        except Exception as e:
            print(e)
            test = False

        return (test, files_exported_count)  # Retourner les deux valeurs


    








  # ... (other methods)

  

    @transaction.atomic
    def import_files_with_codetitre(self, request):
        if request.method == 'POST':
            self.delete_all_files()
            print("Files deleted with success")
            uploaded_files = request.FILES.getlist('imgs[]')  # Replace 'file_0' with the appropriate key
            print("Files = ",uploaded_files)
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
                    print('your uploaded file is = ',uploaded_file)
                    # Create the new filename using unique number and original file name
                    file_name = f"{unique_num}_{uploaded_file}"
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
        print('Not Post request')
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
                    print('Record inserted successfully')

                except Exception as e:
                    print('Exception was occurred')
                    print(e)
                    return '0'
                
                return '1'
        print('Not inserted')
        return '0'








        
    def get_unique_number(self,cursor):
        # Get the current length of the titresimages table
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM titresimages;")
            table_length = cursor.fetchone()[0]

        # Generate a unique number based on table length and current index
        unique_num = table_length + 1  # You can increment the length by 1 to get a unique number

        return unique_num

        


    def display_images(self, request):
        from PIL import Image
        import io
        folder_path = 'D:/tempd/'  # Path to the folder containing TIFF images
        images = []
        codetitre = request.session['session_code_titre']
        count = self.get_count(request)
        
        if self.delete_all_files():  # Execute delete function and check its result
            if self.upload_files_from_database(codetitre):
                image_files = [filename for filename in os.listdir(folder_path)]
        
                print("codetitre =", codetitre)
                for image_file in image_files:
                    file_path_tiff = os.path.join(folder_path, image_file)
        
                    # Check if the file is a TIFF image
                    if file_path_tiff.lower().endswith(".tiff") or file_path_tiff.lower().endswith(".tif"):
                        # Open the TIFF image using PIL
                        tiff_image = Image.open(file_path_tiff)
                        
                        # Convert to PNG format
                        png_image = tiff_image.convert('RGB')
                        
                        # Create an in-memory stream to store the PNG data
                        png_data = io.BytesIO()
                        
                        # Save the PNG image to the in-memory stream
                        png_image.save(png_data, format='PNG')
                        
                        # Get the binary PNG data
                        png_data.seek(0)
                        png_binary = png_data.read()
                        
                        # Convert binary data to base64-encoded string
                        png_base64 = base64.b64encode(png_binary).decode('utf-8')
                        
                        images.append(png_base64)
                        
            else:
                images = []

        return images, count





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

    def find_to_delete(self, request, prefix_value):
        folder_path = 'D:/tempd/'
        num_titre = int(request.session['session_code_titre'])

        try:
            # Retrieve the code_titres from the titres table
            with self.conn.cursor() as cursor1:
                cursor1.execute("SELECT codetitre FROM titres WHERE numtitre = %s;", [num_titre])
                result = cursor1.fetchone()

                if result:
                    code_titre = result[0]

                    file_names = [os.path.splitext(f[2:])[0] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.startswith(str(prefix_value) + '_')]
                    
                    if file_names:
                        file_name = file_names[0]  # Get the first file_name
                        with self.conn.cursor() as cursor2:
                            # Delete the row based on 'code_titre' and 'file_name'
                            print('Im gonna delete ', prefix_value)
                            cursor2.execute("DELETE FROM titresimages WHERE codetitre = %s AND numpage = %s ;", [code_titre, prefix_value])
                            self.conn.commit()  # Commit the transaction

                        # Update the numpage values for images with numpage > prefix_value
                        with self.conn.cursor() as cursor3:
                            cursor3.execute("UPDATE titresimages SET numpage = numpage - 1 WHERE codetitre = %s AND numpage > %s ;", [code_titre, prefix_value])
                            self.conn.commit()

                        return True  # Return True to indicate successful deletion
                    else:
                        return False  # Return False to indicate no file found
                else:
                    return False  # Return False if code_titre is not found
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



    # In your Logical class
    def get_total_users_count(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users_tuser;")
                total_count = cursor.fetchone()[0]
            return total_count
        except Exception as e:
            print("Error:", e)
            return 0  # Return 0 in case of an error


        # In your Logical class
    # Dans votre classe Logical
    def select_users(self, role=None, etat=None):
        selected_users = []  # Liste pour stocker les utilisateurs sélectionnés

        try:
            with self.conn.cursor() as cursor:
                if etat is not None and etat == 1:
                    # Sélectionner tous les utilisateurs si etat est 1
                    cursor.execute("SELECT * FROM users_tuser;")
                elif etat is not None and etat == 0:
                    # Sélectionner les utilisateurs avec etat = 0 et role = 0 si etat est 0
                    cursor.execute("SELECT * FROM users_tuser WHERE etat = 0 AND role = 0;")
                else:
                    # Sélectionner tous les utilisateurs si aucun etat n'est fourni
                    cursor.execute("SELECT * FROM users_tuser;")

                selected_users = cursor.fetchall()  # Récupérer toutes les lignes

            return selected_users  # Retourner la liste des données d'utilisateurs sélectionnées
        except Exception as e:
            print("Erreur :", e)
            return []  # Retourner une liste vide en cas d'erreur




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
            




    def add_new_user(self, username, password, tip, status, address, etat, role):
        import hashlib
        try:
            # Hash the password
            strpwd = password + str(username)
            hashed_password = hashlib.md5(strpwd.encode()).hexdigest()

            # Check if the username already exists
            if self.username_exists(username):
                print("Error: Username already exists")
                return False

            # Find the next available idemp value
            idemp = self.get_next_available_idemp()

            # Insert the user data using a cursor
            with self.conn.cursor() as cursor:
                cursor.execute("INSERT INTO users_tuser (idemp, userauth, passwd, categorie, active, adr_ip, etat, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                            [idemp, username, hashed_password, tip, status, address, etat, role])
                self.conn.commit()

            return True
        except Exception as e:
            print("Error:", e)
            return False

    def username_exists(self, username):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users_tuser WHERE userauth = %s;", [username])
                count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print("Error:", e)
            return False


    def get_next_available_idemp(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT MAX(idemp) FROM users_tuser;")
                max_idemp = cursor.fetchone()[0]
                if max_idemp is None:
                    return 1
                else:
                    return max_idemp + 1
        except Exception as e:
            print("Error:", e)
            return 0


# statistiques  


    def get_stat(self):
            try:
                # Get the counts using a cursor
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM users_tuser;")
                    total_users_count = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM users_tuser WHERE role = 1;")
                    role_1_users_count = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM users_tuser WHERE role = 0;")
                    role_0_users_count = cursor.fetchone()[0]

                # Other code related to your view

                result_list = [
                    total_users_count,
                    role_1_users_count,
                    role_0_users_count,
                    # Other data you want to include in the list
                ]

                return result_list
            
            except Exception as e:
                print("Error:", e)
                return []  # Return an empty list in case of an error

    def get_user_by_idemp(self, idemp):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users_tuser WHERE idemp = %s;", [idemp])
                user_data = cursor.fetchone()
                print(user_data[2])
                return user_data
        except Exception as e:
            print("Error:", e)
            return None

    def update_user_by_idemp(self, idemp, username, password, tip, status, address, etat, role):
        import hashlib
        try:
            # Hash the password
            strpwd = password + str(username)
            hashed_password = hashlib.md5(strpwd.encode()).hexdigest()

            # Perform the update using a cursor
            with self.conn.cursor() as cursor:
                cursor.execute("UPDATE users_tuser SET userauth = %s, passwd = %s, categorie = %s, active = %s, adr_ip = %s, etat = %s, role = %s WHERE idemp = %s;",
                                [username, hashed_password, tip, status, address, etat, role, idemp])
                self.conn.commit()

            return True
        except Exception as e:
            print("Error:", e)
            return False

    def get_user_by_username_password(self, username, password):
        import hashlib
        try:
            # Hash the password using the same method you used during registration
            strpwd = password + str(username)
            hashed_password = hashlib.md5(strpwd.encode()).hexdigest()
            print(hashed_password)
            with self.conn.cursor() as cursorS:
                cursorS.execute("SELECT * FROM users_tuser WHERE userauth = %s AND passwd = %s;", [username, hashed_password])
                user_data = cursorS.fetchone()

            if user_data:
                return user_data
            else:
                return None

        except Exception as e:
            print("Error:", e)
            return None

    # ...

    def change_password(self, old_password, new_password, user_id):
            # Get the username associated with the user ID
            import hashlib
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT userauth FROM users_tuser WHERE idemp = %s;", [user_id])
                username = cursor.fetchone()

                if username:
                    username = username[0]
                    # Hash the user-provided old password with the retrieved username
                    strpwd = old_password + str(username)
                    hashed_old_password = hashlib.md5(strpwd.encode()).hexdigest()

                    # Check if the old password matches the one in the database
                    cursor.execute("SELECT passwd FROM users_tuser WHERE idemp = %s;", [user_id])
                    user_password = cursor.fetchone()

                    if user_password and user_password[0] == hashed_old_password:
                        # Hash the new password before updating it in the database
                        strpwd = new_password + str(username)
                        hashed_new_password = hashlib.md5(strpwd.encode()).hexdigest()

                        # Update the hashed password in the database
                        cursor.execute("UPDATE users_tuser SET passwd = %s WHERE idemp = %s;", [hashed_new_password, user_id])
                        self.conn.commit()
                        return True  # Password changed successfully
                    else:
                        print('Incorrect old password')
                        return False  # Incorrect old password
                else:
                    print('User not found')
                    return False  # User not found



    def display_images_paginations(self, request, posFrom,posTo):

        images = []  

        folder_path = 'D:/tempd/'  # Path to the folder containing images
        codetitre = request.session['session_code_titre']

                # Modify this line to get the count of records for pagination
        count = self.get_count(request)

        if self.delete_all_files():  # Execute delete function and check its result
                result, countImage = self.upload_files_from_database_pages(codetitre, posFrom,posTo)
                if(result) :
                    print('My result id ',result) 
                    image_files = [filename for filename in os.listdir(folder_path)]

                    print("codetitre =", codetitre)

                    # Modify the following loop to use LIMIT and OFFSET
                    for image_file in image_files:
                        file_path_tiff = os.path.join(folder_path, image_file)
                        file_path_png = os.path.splitext(file_path_tiff)[0] + '.png'

                        with self.conn.cursor() as cursor2:
                            # Execute the lo_export query
                            cursor2.execute("SELECT lo_export(doc, %s) FROM titresimages WHERE codetitre = %s ;", [file_path_tiff, codetitre])

    


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
                            print(len(images))
                            #os.remove(file_path_png)

                
        else:
            images = []
            print(len(images))
        print('images = ',images)
        return images, count, countImage


    # protect link 
    def check_user_id(self, request):
            test = False
            # Check if 'user_id' is in the session
            if 'user_id' in request.session:
                user_id = request.session['user_id']
                print('You are connected')
                
                # Manually create a database cursor
                with self.conn.cursor() as cursor:
                    try:
                        # Execute a SQL query to retrieve the user based on user_id
                        cursor.execute("SELECT * FROM users_tuser WHERE idemp = %s", [user_id])
                        user_data = cursor.fetchone()
                        
                        if user_data:
                            # User with the provided id exists
                            test = True
                    except Exception as e:
                        # Handle any database errors
                        messages.error(request, f"Error: {str(e)}")
            
            # If 'user_id' is not in the session or user doesn't exist, return None
            return test
