# iBatis/MyBatis support

This extension handles 
* iBatis 2
* MyBatis 3

# What result can you expect

Creates SQL Named Queries objects for queries found in configuration xml files.
Creates CRUD links to database objects from those queries

# TODO

To be at the same state than xquery+castscript previous implementation
* handle :
  * /sqlMap/statement
  * /sqlMap/procedure
* handle <if> 

* embed jars and add them to classpath (may require autodetect phase)

* create links from Java to Queries
  * iBatis 2
    * add parametrisation rules for classical methods com.ibatis.sqlmap.client.SqlMapClient.insert etc.. 
      see https://ibatis.apache.org/docs/java/user/com/ibatis/sqlmap/client/SqlMapClient.html
  * MyBatis :
    * completely different see https://confluence.castsoftware.com/display/PSTS/J2EE+-+Information+-+MyBatis+3.0,+3.1
     
    
    
    
