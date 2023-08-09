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








  # ... (other methods)

    @transaction.atomic
    def import_files_with_codetitre(self, request):
        if request.method == 'POST' and request.FILES:
            uploaded_files = request.FILES.getlist('files')

            if 'session_code_titre' not in request.session:
                return HttpResponse("Session variable session_code_titre is not set")

            codetitre = request.session['session_code_titre']

            with self.conn.cursor() as cursor:
                for idx, uploaded_file in enumerate(uploaded_files, start=1):
                    # Generate a unique number for each uploaded file
                    unique_num = self.get_unique_number(cursor)

                    # Create the new filename using unique number and original file name
                    file_name = f"{unique_num}_{uploaded_file.name}"
                    file_path = os.path.join('D:/tempd/', file_name)

                    with open(file_path, 'wb') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)

                    try:
                        cursor.execute("""
                            INSERT INTO titresimages (codetitre, doc)
                            VALUES (%s, lo_import(%s))
                        """, [codetitre, file_path])
                        self.conn.commit()
                    except Exception as e:
                        print(e)
                        return 'Some files failed to import'

                return 'Files imported with codetitre values'

        return 'This is not a post request'
    
    def get_unique_number(self, cursor):
        # Get the current length of the titresimages table
        cursor.execute("SELECT COUNT(*) FROM titresimages;")
        table_length = cursor.fetchone()[0]

        # Generate a unique number based on table length and current index
        unique_num = table_length + 1
        return unique_num
    def display_images(self, request):
        folder_path = 'D:/tempd/'  # Path to the folder containing images
        image_files = [filename for filename in os.listdir(folder_path) if filename.lower().endswith(('.tiff', '.tif'))]

        images = []
        codetitre = request.session['session_code_titre']

        for image_file in image_files:
            file_path_tiff = os.path.join(folder_path, image_file)
            file_path_png = os.path.splitext(file_path_tiff)[0] + '.png'

            with self.conn.cursor() as cursor:
                # Execute the lo_export query
                cursor.execute("SELECT lo_export(doc, %s) FROM titresimages WHERE codetitre = %s;", [file_path_tiff, codetitre])

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
        return images