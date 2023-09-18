using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using MyCSharpDatabaseProject;

namespace ConsoleApp1
{
    public class Program
    {
        static void Main(string[] args)
        {
            DatabaseHelper dbHelper = new DatabaseHelper();
            bool result = dbHelper.CheckEmailExists("1234");
            bool result2 = dbHelper.login("1234", "124");
            bool result3 = dbHelper.idrd_check("134");
            bool result4 = dbHelper.InsertUser("12", "12", "상디", "jiskain1124");
            dbHelper.attitude(1, 2);

            // 서버 시작
            Server server = new Server();
            Thread serverThread = new Thread(server.Start);
            serverThread.Start();
            Console.WriteLine("Press Enter to exit...");
            Console.ReadLine();
        }
    }
}
