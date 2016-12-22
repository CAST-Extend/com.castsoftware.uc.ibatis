CREATE TABLE [Employee](
	[Id] [int] NOT NULL,
	[Name] [varchar](60) NULL,
	[DepartmentId] [int] NULL,
	[Age] [tinyint] NULL,
 CONSTRAINT [Pk_Employee] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)
) 

GO