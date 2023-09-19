﻿using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using YourNamespace;
using System.Collections.Generic;
using MyCSharpDatabaseProject;
using System.Text.Json.Nodes;

class Server
{
    private const string FORMAT = "utf-8";
    private const int HEADER_LENGTH = 30;
    private const int BUFFER = 4096;

    public byte[] FixedVolume(string header, string data)
    {
        Console.WriteLine(data.Length);
        byte[] headerBytes = Encoding.GetEncoding(FORMAT).GetBytes(header.PadRight(HEADER_LENGTH));
        byte[] dataBytes = Encoding.GetEncoding(FORMAT).GetBytes(data.PadRight(BUFFER - HEADER_LENGTH));
        return CombineByteArrays(headerBytes, dataBytes);
    }

    private byte[] CombineByteArrays(byte[] first, byte[] second)
    {
        byte[] result = new byte[first.Length + second.Length];
        Buffer.BlockCopy(first, 0, result, 0, first.Length);
        Buffer.BlockCopy(second, 0, result, first.Length, second.Length);
        return result;
    }

    static void Main()
    {

        IPAddress ipAddress = IPAddress.Parse("10.10.20.115");
        int port = 9999;
        Server server = new Server();
        TcpListener listener = new TcpListener(ipAddress, port);
        listener.Start();

        Console.WriteLine("서버가 시작되었습니다. 클라이언트 연결을 대기 중...");

        while (true)
        {
            TcpClient client = listener.AcceptTcpClient();
            NetworkStream stream = client.GetStream();

            Console.WriteLine("클라이언트 연결됨.");

            while (true)
            {
                byte[] data = new byte[4096];
                int bytesRead = stream.Read(data, 0, data.Length);
                string recvMessage = Encoding.UTF8.GetString(data, 0, bytesRead);
                string requestHeader = recvMessage.Substring(0, 30).Trim();
                string requestData = recvMessage.Substring(30).Trim();
                Console.WriteLine($"Server RECEIVED: ({requestHeader},{requestData})");
                Console.WriteLine(requestHeader);
                Console.WriteLine(requestData);

                ObjDecoder objDecoder = new ObjDecoder();
                if (requestHeader == "login_check")
                {
                    object object_ = objDecoder.BinaryToObj(requestData);
                    var dictionary_ = (Dictionary<string, object>)object_;
                    string user_id = (string)dictionary_["user_id"];
                    string user_pw = (string)dictionary_["user_pw"];
                    bool result_ = DatabaseHelper.login(user_id, user_pw);
                    string response_header = "login_check";
                    string response_data = "pass";
                    byte[] return_result = server.FixedVolume(response_header, response_data);
                    stream.Write(return_result, 0, return_result.Length);
                }
                else if (requestHeader == "member_join")
                {
                    string response_header = "member_join";
                    string response_data = ".";
                    byte[] return_result = server.FixedVolume(response_header, response_data);
                    stream.Write(return_result, 0, return_result.Length);
                }

            }
        }
    }
}