import psycopg2
import sys
import logging
#import datetime
from datetime import datetime
                                                                                                                                                                                                                      
class RunDataBaseQ:
    global  NumDemAnnee 
    def __init__(self):
        try:
            self.conn = psycopg2.connect( user = "postgres",
            password = "dbfoncier",
            host = "192.168.1.168",
            port = "5432",
            database = "bdcert")                            
            self.conn.set_client_encoding('WIN1256')  
                  
        except psycopg2.DatabaseError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened successfully.')
              
    def run_query(self,query,curs) :
        try:
            cur=curs        
            records = []
            curs.execute(query)
            result = cur.fetchall()
            for row in result:               
                x={}
                for i in range(len(row)):
                    x[i] = row[i]
                    
                records.append(x)
                self.conn.commit()
                cur.close()
            return jsonify(records)
           
        except psycopg2.DatabaseError as e:
            print(e)                      
        finally:
            if self.conn:
                #self.conn.close()
                logging.info('Database connection closed.')
                
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
    
    def GetListDir(self):
        Sql=''' 
            select ip,libgouv from tgouv where codgouv not in(0,100) and dr=1 order by codgouv
        '''
        curs=self.conn.cursor()
        curs.execute(Sql)
        resultat=curs.fetchall()#self.run_query(Sql,'',curs)
        res = self.getdictres(resultat)
        return res
    
    def GetIpGouv(self,codgouv):   
        Sql='''
        select ip,dir from gouv_ip where gouv= '''+ str(codgouv) +''' order by ordre
        '''
       
        curs=self.conn.cursor()
        curs.execute(Sql)
        resultat=curs.fetchall()#self.run_query(Sql,'',curs)
        res = self.getdictres(resultat)
        return resimport psycopg2
import sys
import logging
#import datetime
from datetime import datetime
                                                                                                                                                                                                                      
class RunDataBaseQ:
    global  NumDemAnnee 
    def __init__(self):
        try:
            self.conn = psycopg2.connect( user = "postgres",
            password = "dbfoncier",
            host = "192.168.1.168",
            port = "5432",
            database = "bdcert")                            
            self.conn.set_client_encoding('WIN1256')  
                  
        except psycopg2.DatabaseError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened successfully.')
              
    def run_query(self,query,curs) :
        try:
            cur=curs        
            records = []
            curs.execute(query)
            result = cur.fetchall()
            for row in result:               
                x={}
                for i in range(len(row)):
                    x[i] = row[i]
                    
                records.append(x)
                self.conn.commit()
                cur.close()
            return jsonify(records)
           
        except psycopg2.DatabaseError as e:
            print(e)                      
        finally:
            if self.conn:
                #self.conn.close()
                logging.info('Database connection closed.')
                
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
    
    def GetListDir(self):
        Sql=''' 
            select ip,libgouv from tgouv where codgouv not in(0,100) and dr=1 order by codgouv
        '''
        curs=self.conn.cursor()
        curs.execute(Sql)
        resultat=curs.fetchall()#self.run_query(Sql,'',curs)
        res = self.getdictres(resultat)
        return res
    
    def GetIpGouv(self,codgouv):   
        Sql='''
        select ip,dir from gouv_ip where gouv= '''+ str(codgouv) +''' order by ordre
        '''
       
        curs=self.conn.cursor()
        curs.execute(Sql)
        resultat=curs.fetchall()#self.run_query(Sql,'',curs)
        res = self.getdictres(resultat)
        return res