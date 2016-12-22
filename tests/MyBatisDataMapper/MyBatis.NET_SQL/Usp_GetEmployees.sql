CREATE PROCEDURE GetEmployees 
(
  @DepartmentId Int
)
AS

SELECT Id, Name, Age, DepartmentId FROM Employee WHERE DepartmentId = @DepartmentId
 