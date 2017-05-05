import cast_upgrade_1_5_3 # @UnusedImport
import cast.analysers.jee
import cast.analysers.dotnet
from cast.analysers import log, CustomObject, external_link, create_link
import xml.etree.ElementTree as ET

#TODO
# Perf
# Namespace for MyBatis.NET

class MyBatis3SQLNamedQuery(cast.analysers.jee.Extension):
    
    def start_analysis(self, options):
        log.info('Register MyBatis3 xml file pattern')
        options.handle_xml_with_xpath('//mapper')

    def start_xml_file(self, file):        
        tree = ET.ElementTree(file=open(file.get_path()))
        root=tree.getroot()
        if root.tag != 'mapper':
            pass
        else:                        
            log.info('Scanning MyBatis3 file: %s' % file.get_path())
            typeAliases = TypeAliases.parse(root)
            
            resultMaps = ResultMaps.parse(root, typeAliases)
            
            sql_queries = CommonParsing.get_sql_queries(root)
            
            statement_queries = CommonParsing.get_statement_queries(root)
            CommonParsing.add_sqlnamedquery(statement_queries, sql_queries, resultMaps, typeAliases, file, root.attrib['namespace'])
                
            procedure_queries = CommonParsing.get_procedure_queries(root)
            CommonParsing.add_sqlnamedquery(procedure_queries, sql_queries, resultMaps, typeAliases, file, root.attrib['namespace'])
            
            select_queries = CommonParsing.get_select_queries(root)
            CommonParsing.add_sqlnamedquery(select_queries, sql_queries, resultMaps, typeAliases, file, root.attrib['namespace'])
            
            insert_queries = CommonParsing.get_insert_queries(root)
            CommonParsing.add_sqlnamedquery(insert_queries, sql_queries, resultMaps, typeAliases, file, root.attrib['namespace'])  
            
            update_queries = CommonParsing.get_update_queries(root)          
            CommonParsing.add_sqlnamedquery(update_queries, sql_queries, resultMaps, typeAliases, file, root.attrib['namespace'])            
            
            delete_queries = CommonParsing.get_delete_queries(root)
            CommonParsing.add_sqlnamedquery(delete_queries, sql_queries, resultMaps, typeAliases, file, root.attrib['namespace'])        


class iBatis2SQLNamedQuery(cast.analysers.jee.Extension):
    
    def start_analysis(self, options):
        log.info('Register iBatis2 file pattern')
        options.handle_xml_with_xpath('//sqlMap')

    def start_xml_file(self, file):       
        tree = ET.ElementTree(file=open(file.get_path()))
        root=tree.getroot()
        if root.tag != 'sqlMap':
            pass
        else:
            log.info('Scanning iBatis2 file: %s' % file.get_path())
            typeAliases = TypeAliases.parse(root)
            
            resultMaps = ResultMaps.parse(root, typeAliases)
            
            sql_queries = CommonParsing.get_sql_queries(root)
            
            statement_queries = CommonParsing.get_statement_queries(root)
            CommonParsing.add_sqlnamedquery(statement_queries, sql_queries, resultMaps, typeAliases, file, '')
                
            procedure_queries = CommonParsing.get_procedure_queries(root)
            CommonParsing.add_sqlnamedquery(procedure_queries, sql_queries, resultMaps, typeAliases, file, '')
            
            select_queries = CommonParsing.get_select_queries(root)
            CommonParsing.add_sqlnamedquery(select_queries, sql_queries, resultMaps, typeAliases, file, '')
            
            insert_queries = CommonParsing.get_insert_queries(root)
            CommonParsing.add_sqlnamedquery(insert_queries, sql_queries, resultMaps, typeAliases, file, '')  
            
            update_queries = CommonParsing.get_update_queries(root)          
            CommonParsing.add_sqlnamedquery(update_queries, sql_queries, resultMaps, typeAliases, file, '')            
            
            delete_queries = CommonParsing.get_delete_queries(root)
            CommonParsing.add_sqlnamedquery(delete_queries, sql_queries, resultMaps, typeAliases, file, '')                    

            
class iBatis2DotNetSQLNamedQuery(cast.analysers.dotnet.Extension):
    
    def start_analysis(self, options):
        log.info('iBatis.NET extension loaded')
    
    def start_file(self, file):
        if file.get_name().endswith('xml'):
            log.debug('Found xml file: %s' % file.get_path())
            tree = ET.parse(file.get_path(), ET.XMLParser(encoding="utf-8"))
            root=tree.getroot()
            if root.tag == 'sqlMap' or root.tag == '{http://ibatis.apache.org/mapping}sqlMap' :
                log.info('Scanning iBatis.NET file: %s' % file.get_name())
                
                typeAliases = TypeAliases.parse(root)
                
                resultMaps = ResultMaps.parse(root, typeAliases)
                     
                sql_queries = CommonParsing.get_sql_queries(root)
                     
                statement_queries = CommonParsing.get_statement_queries(root)
                CommonParsing.add_sqlnamedquery(statement_queries, sql_queries, resultMaps, typeAliases, file, '')
                
                procedure_queries = CommonParsing.get_procedure_queries(root)
                CommonParsing.add_sqlnamedquery(procedure_queries, sql_queries, resultMaps, typeAliases, file, '')
                
                select_queries = CommonParsing.get_select_queries(root)
                CommonParsing.add_sqlnamedquery(select_queries, sql_queries, resultMaps, typeAliases, file, '')
                
                insert_queries = CommonParsing.get_insert_queries(root)
                CommonParsing.add_sqlnamedquery(insert_queries, sql_queries, resultMaps, typeAliases, file, '')  
                
                update_queries = CommonParsing.get_update_queries(root)          
                CommonParsing.add_sqlnamedquery(update_queries, sql_queries, resultMaps, typeAliases, file, '')            
                
                delete_queries = CommonParsing.get_delete_queries(root)
                CommonParsing.add_sqlnamedquery(delete_queries, sql_queries, resultMaps, typeAliases, file, '')

class TypeAliases():
    @staticmethod
    def parse(root):
        result = {}
    
        for node in root.findall('.//{http://ibatis.apache.org/mapping}typeAlias'):
            if 'type' in node.attrib:          
                result[node.attrib['alias']] = node.attrib['type'].split(",")[0]
        
        for node in root.findall('.//typeAlias'):
            if 'type' in node.attrib: 
                result[node.attrib['alias']] = node.attrib['type'].split(",")[0]
        
        #log.info('Aliases')
        #for aliasId, aliasType in result.items():
        #    log.info(' - %s: %s' % (aliasId, aliasType)) 
        return result
                    
class ResultMaps():
    @staticmethod
    def parse(root, typeAliases):
        result = {}
    
        for node in root.findall('.//{http://ibatis.apache.org/mapping}resultMap'):
            if 'class' in node.attrib:  
                if node.attrib['class'] in typeAliases:
                    result[node.attrib['id']] = typeAliases[node.attrib['class']]
                else:     
                    result[node.attrib['id']] = node.attrib['class']
        
        for node in root.findall('.//resultMap'):
            if 'class' in node.attrib: 
                if node.attrib['class'] in typeAliases:
                    result[node.attrib['id']] = typeAliases[node.attrib['class']]
                else:     
                    result[node.attrib['id']] = node.attrib['class']
           
        return result

class CommonParsing():
    @staticmethod
    def get_select_queries(root):
        return CommonParsing.get_queries_by_type(root, 'select')
    @staticmethod
    def get_statement_queries(root):
        return CommonParsing.get_queries_by_type(root, 'statement') 
    @staticmethod
    def get_procedure_queries(root):
        return CommonParsing.get_queries_by_type(root, 'procedure') 
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
    
        for node in root.findall('.//{http://ibatis.apache.org/mapping}' + str_type):
            result[node.attrib['id']] = node
        
        for node in root.findall('.//' + str_type):
            result[node.attrib['id']] = node 
        return result
    
    @staticmethod
    def add_sqlnamedquery(sqltable, sql_queries, resultMaps, typeAliases, file, namespace):
        for sqlid, node in sqltable.items():
            log.info('NEW Named Query - %s' % sqlid)            
            
            sqlquery = CustomObject()
            sqlquery.set_name(sqlid)
            sqlquery.set_type('CAST_SQL_NamedQuery')
            sqlquery.set_parent(file)
            sqlquery.save()
            
            #Get SQL from node
            sql = node.text
            for sub_node in node:
                if 'refid' in sub_node.attrib and sub_node.attrib['refid'] in sql_queries:
                    sql += sql_queries[sub_node.attrib['refid']].text.strip()
                if sub_node.tail:
                    sql += sub_node.tail
            
            #log.info('SQL: %s' % sql)
            sqlquery.save_property('CAST_SQL_MetricableQuery.sqlQuery', sql)
            
            log.info(' - creating links...')
            for embedded in external_link.analyse_embedded(sql):
                for t in embedded.types:
                    #log.info(' - link to : %s' % embedded.callee.get_name())
                    create_link(t, sqlquery, embedded.callee)
            
            #Save all potential properties for later use
            CommonParsing.add_property(sqlquery, node, 'parameterClass', typeAliases)
            CommonParsing.add_property(sqlquery, node, 'parameterType', typeAliases)
            CommonParsing.add_property(sqlquery, node, 'resultClass', typeAliases)
            CommonParsing.add_property(sqlquery, node, 'listClass', typeAliases)
            CommonParsing.add_property(sqlquery, node, 'resultMap', typeAliases)
            CommonParsing.add_property(sqlquery, node, 'resultType', typeAliases)
            CommonParsing.add_property(sqlquery, node, 'parameterMap', typeAliases)
            
            if (namespace != ''):
                log.debug('Habemus namespacus!')
                sqlquery.save_property('iBatisProperties.namespace', namespace)
            
            for mapId, mapClass in resultMaps.items():
                if 'resultMap' in node.attrib and node.attrib['resultMap'] == mapId:
                    log.debug(' - class: %s' % mapClass)
                    sqlquery.save_property('iBatisProperties.class', mapClass)
    
    @staticmethod
    def add_property(sqlquery, node, prop, typeAliases):
        if prop in node.attrib:
            if node.attrib[prop] in typeAliases:
                log.debug(' - %s: %s' % (prop, typeAliases[node.attrib[prop]]))
                sqlquery.save_property('iBatisProperties.%s' % prop, typeAliases[node.attrib[prop]])
            else:
                log.debug(' - %s: %s' % (prop, node.attrib[prop]))
                sqlquery.save_property('iBatisProperties.%s' % prop, node.attrib[prop])
            