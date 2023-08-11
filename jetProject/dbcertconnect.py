import psycopg2
import sys
import logging
#import datetime

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


class LogicalDB : 
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
    #def __init__(self):
    #    try:
    #        self.conn = psycopg2.connect( user = "postgres",
    #        password = "dbfoncier",
    #        host = "192.168.1.168",
    #        port = "5432",
    #        database = "bdcert")                            
    #        self.conn.set_client_encoding('WIN1256')  
                  
    #    except psycopg2.DatabaseError as e:
    #        logging.error(e)
    #        sys.exit()
    #    finally:
    #        logging.info('Connection opened successfully.')

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
            select codgouv, libgouv, dr from tgouv where codgouv not in (0, 100) order by codgouv
        '''
        curs = self.conn.cursor()
        curs.execute(Sql)
        resultat = curs.fetchall()
        res = self.getdictres(resultat)
        return res

    def GetTitreExiste(self,numtitre,gouvtitre,doubtitre,dreg):       
        if gouvtitre=="0":
            gouvtitre=0
        if doubtitre==" ":
            doubtitre=0     
    
        xquery=(''' SELECT numtitre,gouvtitre,doubtitre,dreg from tfich where numtitre = ''' + str(numtitre) + ''' and gouvtitre = '''+ str(gouvtitre) +''' and doubtitre = '''+ str(doubtitre) +'''  and dreg='''+ str(dreg) +''' and typfiche=1''')
        #return xquery
        curs=self.conn.cursor()   
        curs.execute(xquery)
        rows = curs.fetchall() 
          
        if len(rows)  > 0 :
            for row in rows:
                iquery=('''SELECT * from tfich where numtitre = '''+ str(row[0]) +''' and gouvtitre = '''+ str(row[1]) +''' and doubtitre = '''+ str(row[2]) +'''  and dreg='''+ str(row[3]) +''' and typfiche=3''')
                cur1=self.conn.cursor()   
                cur1.execute(iquery)
                irows = cur1.fetchall()  
                #self.conn1.close()        
                if len(irows) > 0 :                     
                    return "2"                   
                else: 
                    return "1"                                         
        else:
            return "0"
    def Increment_num_titre(self):
        numtitre = 0
        max_numtitre_query = "SELECT MAX(numtitre) FROM titres"
        cursor = self.conn.cursor()
        cursor.execute(max_numtitre_query)
        max_numtitre = cursor.fetchone()[0]
        if max_numtitre is not None:
            numtitre = max_numtitre + 1  # Increment by 1
        return numtitre

    def ajouter_titre(self, numtitre, gouvtitre, doubtitre, nbpage):
        test = False
        # Check if the title exists in the distant server
        response_data = self.GetTitreExiste(numtitre, gouvtitre, doubtitre, 9) 
        # Test if title exists in the distant server
        print("response_data = ",response_data)
        if response_data == "1" or response_data == "2": 
            print('oui') 
            insert_query = '''INSERT INTO titres (numtitre, gouvtitre, doubtitre, nbpage) VALUES (%s, %s, %s, %s)'''
            cursor = self.conn.cursor()
            cursor.execute(insert_query, [numtitre, gouvtitre, doubtitre, nbpage])
            self.conn.commit()
            test = True
        return test
       
       
            
        



