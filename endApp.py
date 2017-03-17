import cast_upgrade_1_5_3 # @UnusedImport
from cast.application import ApplicationLevelExtension, create_link, ReferenceFinder
import logging

class ApplicationExtension(ApplicationLevelExtension):

    def end_application(self, application):
        logging.info('Creating links to iBatis objects...')
        
        for classObject in application.objects().has_type([ 'CAST_DotNet_ConstructorCSharp',
                                                            'CAST_DotNet_ConstructorExternal',
                                                            'CAST_DotNet_ConstructorVB',
                                                            'JV_CTOR',
                                                            'JV_GENERIC_CTOR',
                                                            'JV_INST_CTOR']):
            #logging.debug('WTF %s.%s' % (namedQuery.get_property(prop), classObject.get_name()))
            iBatisLinks.create(application, classObject)
        
        for methodObject in application.search_objects(category='JV_METHOD', load_properties=True):
            MyBatisLinks.create(application, methodObject)                        
        
        #GREP in DotNet/Java, looking for iBatis objects
        rf = ReferenceFinder()
        rf.add_pattern('iBatis', before='["\.]', element='[A-Za-z0-9_\-]+', after='"')
        
        references = []
        for o in application.get_files(['CAST_DotNet_CSharpFile', 'JV_FILE']):             
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
             
            references += [reference for reference in rf.find_references_in_file(o)]
            
        for reference in references:
            for namedQuery in application.objects().has_type('CAST_SQL_NamedQuery'):
                if reference.value == namedQuery.get_name():
                    logging.debug('Reference to %s found in %s' % (namedQuery.get_name(), reference.object.get_name()))
                    create_link('callLink', reference.object, namedQuery, reference.bookmark)

class MyBatisLinks():                
    @staticmethod
    def create(application, methodObject):
        for namedQuery in application.search_objects(category='CAST_SQL_NamedQuery', load_properties=True):
            #logging.debug('MYBATIS %s == %s.%s' % (methodObject.get_fullname(), namedQuery.get_property('iBatisProperties.namespace'), namedQuery.get_name()));
            if methodObject.get_fullname() == '%s.%s' % (namedQuery.get_property('iBatisProperties.namespace'), namedQuery.get_name()):
                logging.debug('MyBatis structural link from %s to %s' % (methodObject.get_fullname(), namedQuery.get_name()))
                create_link('useLink', methodObject, namedQuery)
    
class iBatisLinks():
    @staticmethod
    def create(application, classObject):
        for namedQuery in application.search_objects(category='CAST_SQL_NamedQuery', load_properties=True):
            iBatisLinks.createForProp(application, classObject, namedQuery, 'iBatisProperties.class')
            iBatisLinks.createForProp(application, classObject, namedQuery, 'iBatisProperties.parameterClass')
            iBatisLinks.createForProp(application, classObject, namedQuery, 'iBatisProperties.resultClass')
            iBatisLinks.createForProp(application, classObject, namedQuery, 'iBatisProperties.listClass')
            iBatisLinks.createForProp(application, classObject, namedQuery, 'iBatisProperties.resultType')
            
    @staticmethod
    def createForProp(application, classObject, namedQuery, prop):
        if classObject.get_fullname() == '%s.%s' % (namedQuery.get_property(prop), classObject.get_name()):
            logging.debug('iBatis structural link from %s to %s' % (namedQuery.get_name(), classObject.get_fullname()))
            create_link('referLink', namedQuery, classObject)
