/*using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading.Tasks;*/

/*namespace ConsoleApp1
{
    public class Server
    {
        public void Start()
        {
            while (true) 
            { 
                try
                {
                    string serverIP = "127.0.0.1";
                    int serverPort = 9999;

                    TcpListener listener = new TcpListener(IPAddress.Parse(serverIP), serverPort);
                    listener.Start();
                    Console.WriteLine("서버 대기 중...");

                    using (TcpClient client = listener.AcceptTcpClient())
                    {
                        Console.WriteLine("클라이언트 연결됨.");

                        using (NetworkStream stream = client.GetStream())
                        {
                            byte[] buffer = new byte[1024];
                            int bytesRead = stream.Read(buffer, 0, buffer.Length);
                            string clientMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                            Console.WriteLine("클라이언트 메시지: " + clientMessage);

                            string responseMessage = "안녕하세요, 클라이언트!";
                            byte[] responseData = Encoding.UTF8.GetBytes(responseMessage);
                            stream.Write(responseData, 0, responseData.Length);
                            Console.WriteLine("응답 전송: " + responseMessage);
                        }
                    }
                }

                catch (Exception ex)
                {
                    Console.WriteLine("오류: " + ex.Message);
                }
            }
        }
    }
}*/
using System;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;


namespace ConsoleApp1
{
    public class Server
    {
        private const string HOST = "127.0.0.1";
        private const int PORT = 9999;
        private const int BUFFER = 50000;
        private const string FORMAT = "utf-8";
        private const int HEADER_LENGTH = 30;

        private const string log_in = "log_in";
        private const string PASS_ENCODED = "pass";
        private const string DOT_ENCODED = ".";

        private Socket serverSocket;
        private List<Socket> socketsList;
        private Dictionary<Socket, string> clients;
        private Thread threadForRun;
        private bool runSignal;

        public Server()
        {
            serverSocket = null;
            socketsList = new List<Socket>();
            clients = new Dictionary<Socket, string>();
            threadForRun = null;
            runSignal = true;
        }

        public void SetConfig(string configure)
        {
            // 서버 설정 적용 코드
            Console.WriteLine("서버 설정 적용됨");
        }

        public void Start()
        {
            if (threadForRun != null)  // 실행중이면 종료 시키기
            {
                return;
            }

            serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            serverSocket.Bind(new IPEndPoint(IPAddress.Parse(HOST), PORT));
            serverSocket.Listen(5);
            socketsList.Clear();
            socketsList.Add(serverSocket);
            runSignal = true;
            threadForRun = new Thread(Run);
            threadForRun.Start();
        }

        public void Stop()
        {
            runSignal = false;
            if (threadForRun != null)
            {
                threadForRun.Join();
            }
            serverSocket.Close();
            threadForRun = null;
        }

        private void Run()
        {
            while (true)
            {
                if (!runSignal)
                {
                    break;
                }

                try
                {
                    List<Socket> readSockets = new List<Socket>();
                    List<Socket> exceptionSockets = new List<Socket>();

                    Socket.Select(socketsList, readSockets, null, 100000);

                    foreach (Socket notifiedSocket in readSockets)
                    {
                        if (notifiedSocket == serverSocket)
                        {
                            Socket clientSocket = serverSocket.Accept();
                            socketsList.Add(clientSocket);
                        }
                        else
                        {
                            string message = ReceiveMessage(notifiedSocket);

                            if (message == null)
                            {
                                socketsList.Remove(notifiedSocket);
                            }
                        }
                    }

                    foreach (Socket exceptionSocket in exceptionSockets)
                    {
                        socketsList.Remove(exceptionSocket);
                        clients.Remove(exceptionSocket);
                    }
                }
                catch (Exception)
                {
                    continue;
                }
            }
        }

        public void SendMessage(Socket clientSocket, byte[] result)
        {
            clientSocket.Send(result);
        }

        public byte[] FixedVolume(string header, string data)
        {
            string headerMsg = header.PadRight(HEADER_LENGTH);
            string dataMsg = data.PadRight(BUFFER - HEADER_LENGTH);
            byte[] headerBytes = Encoding.UTF8.GetBytes(headerMsg);
            byte[] dataBytes = Encoding.UTF8.GetBytes(dataMsg);
            byte[] result = new byte[BUFFER];
            Array.Copy(headerBytes, 0, result, 0, HEADER_LENGTH);
            Array.Copy(dataBytes, 0, result, HEADER_LENGTH, BUFFER - HEADER_LENGTH);
            return result;
        }

        public string ReceiveMessage(Socket clientSocket)
        {
            byte[] recvMessageBytes = new byte[BUFFER];
            int bytesRead;

            try
            {
                bytesRead = clientSocket.Receive(recvMessageBytes);
                Console.WriteLine("start");
            }
            catch (SocketException)
            {
                return null;
            }

            if (bytesRead == 0)
            {
                return null;
            }

            string recvMessage = Encoding.UTF8.GetString(recvMessageBytes, 0, bytesRead);
            string requestHeader = recvMessage.Substring(0, HEADER_LENGTH).Trim();
            string requestData = recvMessage.Substring(HEADER_LENGTH).Trim();
            Console.WriteLine($"Server RECEIVED: ({requestHeader},{requestData})");
            Console.WriteLine(requestHeader);
            Console.WriteLine(requestHeader.GetType());

            return recvMessage;
        }
    }
}