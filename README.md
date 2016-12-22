# iBatis/MyBatis support

This extension handles 
* iBatis 2
* MyBatis 3
* iBatis.NET

# What result can you expect

Creates SQL Named Queries objects for queries found in configuration xml files.
Creates CRUD links to database objects from those queries
Links from SQL Named Queries to classes referenced in configuration file (class, resultMap, etc...)
Links from .NET/JAVA to SQL Named Queries

# TODO

To be at the same state than xquery+castscript previous implementation
* handle <if> 

* embed jars and add them to classpath (may require autodetect phase)

* create a security rule for potential SQL injection due to $ parameters - 
http://software-security.sans.org/developer-how-to/fix-sql-injection-in-java-mybatis
     
    
    
    
