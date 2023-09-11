using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    public class Program
    {
        static void Main(string[] args)
        {
            // 서버 시작
            Server server = new Server();
            Thread serverThread = new Thread(server.Start);
            serverThread.Start();

            Console.WriteLine("Press Enter to exit...");
            Console.ReadLine();
        }
    }
}
