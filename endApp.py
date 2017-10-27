import cast_upgrade_1_5_14 # @UnusedImport
from cast.application import ApplicationLevelExtension, create_link, ReferenceFinder
import logging

class ApplicationExtension(ApplicationLevelExtension):

    def end_application(self, application):
        logging.info('Creating links to iBatis objects...')
        
        for namedQuery in application.search_objects(category='CAST_SQL_NamedQuery', load_properties=True):
            logging.debug('Processing Name query %s' % namedQuery.get_name())
            
            iBatisLinks.create(application, namedQuery, 'iBatisProperties.class')
            iBatisLinks.create(application, namedQuery, 'iBatisProperties.parameterClass')
            iBatisLinks.create(application, namedQuery, 'iBatisProperties.resultClass')
            iBatisLinks.create(application, namedQuery, 'iBatisProperties.listClass')
            iBatisLinks.create(application, namedQuery, 'iBatisProperties.resultType')
            MyBatisLinks.create(application, namedQuery)                    
        
        #GREP in DotNet/Java, looking for iBatis objects
        logging.info('Creating dynamic links to iBatis objects...')
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
                    link = create_link('callLink', reference.object, namedQuery, reference.bookmark)
                    link.mark_as_not_sure()

class MyBatisLinks():                
    @staticmethod
    def create(application, namedQuery):
        # @todo : inefficient : this a unitary query inside a loop
        logging.debug('Looking for %s' % namedQuery.get_name())     
        for methodObject in application.search_objects(name=namedQuery.get_name(), category='JV_METHOD'):
            if methodObject.get_fullname() == '%s.%s' % (namedQuery.get_property('iBatisProperties.namespace'), namedQuery.get_name()):
                logging.debug('MyBatis structural link from %s to %s' % (methodObject.get_fullname(), namedQuery.get_name()))
                link = create_link('useLink', methodObject, namedQuery)
                link.mark_as_not_sure()

class iBatisLinks():
    @staticmethod
    def create(application, namedQuery, prop):
        if namedQuery.get_property(prop) is None:
            return
        
        if namedQuery.get_property(prop).find('.') == -1:
            classname = namedQuery.get_property(prop)
        else:
            classname = namedQuery.get_property(prop).split('.')[-1]
        
        logging.debug('Looking for %s' % classname)
        for constructorObject in application.search_objects(name=classname, category='CAST_DotNet_ConstructorCSharp'):
            iBatisLinks.create_iBatisLink(application, namedQuery, prop, classname, constructorObject)
        for constructorObject in application.search_objects(name=classname, category='CAST_DotNet_ConstructorExternal'):
            iBatisLinks.create_iBatisLink(application, namedQuery, prop, classname, constructorObject) 
        for constructorObject in application.search_objects(name=classname, category='CAST_DotNet_ConstructorVB'):
            iBatisLinks.create_iBatisLink(application, namedQuery, prop, classname, constructorObject) 
        for constructorObject in application.search_objects(name=classname, category='JV_CTOR'):
            iBatisLinks.create_iBatisLink(application, namedQuery, prop, classname, constructorObject) 
        for constructorObject in application.search_objects(name=classname, category='JV_GENERIC_CTOR'):
            iBatisLinks.create_iBatisLink(application, namedQuery, prop, classname, constructorObject) 
        for constructorObject in application.search_objects(name=classname, category='JV_INST_CTOR'):
            iBatisLinks.create_iBatisLink(application, namedQuery, prop, classname, constructorObject)      
    
    @staticmethod
    def create_iBatisLink(application, namedQuery, prop, classname, constructorObject):  
        if constructorObject.get_fullname() == '%s.%s' % (namedQuery.get_property(prop), classname):
            logging.debug('iBatis structural link from %s to %s' % (namedQuery.get_name(), constructorObject.get_fullname()))
            link = create_link('referLink', namedQuery, constructorObject)
            link.mark_as_not_sure()