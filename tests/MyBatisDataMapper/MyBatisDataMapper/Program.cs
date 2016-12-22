using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using IBatisNet.Common;
using IBatisNet.DataMapper;


namespace MyBatisDataMapper
{
    class Program
    {
        public static ISqlMapper EntityMapper
        {
            get
            {
                try
                {
                    ISqlMapper mapper = Mapper.Instance();
                    return mapper;
                }
                catch (Exception ex)
                {
                    throw ex;
                }
            }
        }


        public static List<model.Employee> getEmployees(model.Department department)
        {

            ISqlMapper mapper = EntityMapper;

            List<model.Employee> employees = mapper.QueryForList<model.Employee>("GetEmployees", department).ToList();
            return employees;


        }

        public static string FindDepartment(int deptId){

            ISqlMapper mapper = EntityMapper;
            string str = mapper.QueryForObject<string>("FindDepartment", deptId);
            return str;


        }


        static void Main(string[] args)
        {
            
            //Find Department
            string deptName = FindDepartment(1);
            Console.WriteLine(deptName);
            Console.Read();
            
            // Get Employees
            model.Department dep = new model.Department();
            dep.Id = 1;
            List<model.Employee> emps = getEmployees(dep);
            Console.ReadLine();

            
        }
    }
}
