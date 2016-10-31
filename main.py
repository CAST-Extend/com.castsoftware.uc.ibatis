import cast.analysers.jee
from cast.analysers import log, CustomObject, external_link, create_link
import xml.etree.ElementTree as ET


class MyBatis3SQLNamedquery(cast.analysers.jee.Extension):
    
    def start_analysis(self, options):
        log.info('start_analysis MyBatis3')
        options.handle_xml_with_xpath('//mapper')

    def start_xml_file(self, file):
        log.info('scanning file %s for MyBatis3' % file.get_path())
        
        tree = ET.ElementTree(file=open(file.get_path()))
        root=tree.getroot()
        if root.tag != 'mapper':
            pass
        else:
            select_queries = CommonParsing.get_select_queries(root)
            CommonParsing.add_sqlnamedquery(select_queries, file)
            insert_queries = CommonParsing.get_insert_queries(root)
            CommonParsing.add_sqlnamedquery(insert_queries, file)            
            delete_queries = CommonParsing.get_delete_queries(root)
            CommonParsing.add_sqlnamedquery(delete_queries, file)        
            #sql_queries = CommonParsing.get_sql_queries(root)
            #CommonParsing.add_sqlnamedquery(sql_queries, file)       


class iBatis2SQLNamedquery(cast.analysers.jee.Extension):
    
    def start_analysis(self, options):
        log.info('start_analysis iBatis2')
        options.handle_xml_with_xpath('//sqlMap')

    def start_xml_file(self, file):
        log.info('scanning file %s for iBatis2' % file.get_path())
        
        tree = ET.ElementTree(file=open(file.get_path()))
        root=tree.getroot()
        if root.tag != 'sqlMap':
            pass
        else:
            select_queries = CommonParsing.get_select_queries(root)
            CommonParsing.add_sqlnamedquery(select_queries, file)
            insert_queries = CommonParsing.get_insert_queries(root)
            CommonParsing.add_sqlnamedquery(insert_queries, file)  
            update_queries = CommonParsing.get_update_queries(root)          
            CommonParsing.add_sqlnamedquery(update_queries, file)            
            delete_queries = CommonParsing.get_delete_queries(root)
            CommonParsing.add_sqlnamedquery(delete_queries, file)                    
            #sql_queries = CommonParsing.get_sql_queries(root)
            #CommonParsing.add_sqlnamedquery(sql_queries, file)       

class CommonParsing():
    @staticmethod
    def get_select_queries(root):
        return CommonParsing.get_queries_by_type(root, 'select') 
    @staticmethod
    def get_insert_queries(root):
        return CommonParsing.get_queries_by_type(root, 'insert') 
    @staticmethod
    def get_update_queries(root):
        return CommonParsing.get_queries_by_type(root, 'update') 
    @staticmethod
    def get_delete_queries(root):
        return CommonParsing.get_queries_by_type(root, 'delete') 
    @staticmethod
    def get_sql_queries(root):
        return CommonParsing.get_queries_by_type(root, 'sql') 
    @staticmethod     
    def get_queries_by_type(root, str_type):
        result = {}
    
        for node in root.findall('.//' + str_type):
            select_text = node.text
            for sub_node in node:
                select_text += sub_node.tail
            
            result[node.attrib['id']] = select_text
        return result
    
    @staticmethod
    def add_sqlnamedquery(sqltable, file):
        for sqlid, sql in sqltable.items():
            log.info('id %s' % sqlid)
            log.info('sql %s' % sql)
            sqlquery = CustomObject()
            sqlquery.set_name(sqlid)
            sqlquery.set_type('CAST_SQL_NamedQuery')
            sqlquery.set_parent(file)
            sqlquery.save()
            sqlquery.save_property("CAST_SQL_MetricableQuery.sqlQuery", sql)
            
            for embedded in external_link.analyse_embedded(sql):
                for t in embedded.types:
                    create_link(t, sqlquery, embedded.callee)