using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using Npgsql;

namespace MyCSharpDatabaseProject
{

    public class DatabaseHelper
    {
        static void Main()
        {
            DatabaseHelper dbHelper = new DatabaseHelper();
            bool result = dbHelper.CheckEmailExists("1234");
            bool result2 = dbHelper.login("1234", "124");
            bool result3 = dbHelper.idrd_check("134");
            dbHelper.attitude(1, 2);
            //bool result = dbHelper.InsertUser()
        }


        private readonly NpgsqlConnection pgdb;

        // PostgreSQL 데이터베이스 연결 정보 설정
        public DatabaseHelper()
        {
            string connectionString = "Host=10.10.20.114;Database=pirates;Username=postgres;Password=ilsan1236526";
            pgdb = new NpgsqlConnection(connectionString);
        }

        // 접속자의 회원정보 반환 input-> 회원 아이디
        public bool CheckEmailExists(string InputID)
        {
            try
            {
                pgdb.Open(); // 데이터베이스 연결 열기
                using (NpgsqlCommand cmd = new NpgsqlCommand())
                {
                    cmd.Connection = pgdb;
                    cmd.CommandText = "SELECT * FROM public.\"TB_USER\" WHERE \"USER_ID\" = @InputID;";
                    cmd.Parameters.AddWithValue("InputID", InputID);

                    using (var reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            int firstName = (int)reader.GetValue(0);
                            string lastName = reader.GetString(1);
                            string email = reader.GetString(2);
                            string email2 = reader.GetString(3);
                            string email3 = reader.GetString(4);
                            Console.WriteLine($"코드: {firstName}, 아이디:{lastName} 비밀번호: {email}, 이름: {email2}, 부모:{email3}");
                        }
                        return !reader.HasRows; // true if email doesn't exist, false if it does
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return false; // 예외 처리: 데이터베이스 오류가 발생한 경우 false 반환
            }
            finally
            {
                pgdb.Close(); // 데이터베이스 연결 닫기 (finally 블록은 항상 실행됨)
            }
        }

        // 회원가입: 회원가입 성공여부 결과를 true, false로 보낸다
        public bool InsertUser(string user_id, string user_pw, string user_name, string user_parent)
        {
            try
            {
                pgdb.Open(); // 데이터베이스 연결 열기
                using (NpgsqlCommand cmd = new NpgsqlCommand())
                {
                    cmd.Connection = pgdb;
                    cmd.CommandText = "INSERT INTO public.\"TB_USER\" (\"USER_ID\", \"USER_PW\", \"USER_NAME\", \"USER_PARENS\") " +
                                      "VALUES (@ID, @Password, @name, @parent);";
                    cmd.Parameters.AddWithValue("ID", user_id);
                    cmd.Parameters.AddWithValue("Password", user_pw);
                    cmd.Parameters.AddWithValue("name", user_name);
                    cmd.Parameters.AddWithValue("parent", user_parent);

                    return true; // true if insertion was successful, false otherwise
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return false; // 예외 처리: 데이터베이스 오류가 발생한 경우 false 반환
            }
            finally
            {
                pgdb.Close(); // 데이터베이스 연결 닫기 (finally 블록은 항상 실행됨)
            }
        }

        //로그인 결과 반환 
        public bool login(string user_id, string user_pw)
        {
            try
            {
                pgdb.Open(); // 데이터베이스 연결 열기
                using (NpgsqlCommand cmd = new NpgsqlCommand())
                {
                    cmd.Connection = pgdb;
                    cmd.CommandText = "SELECT * FROM public.\"TB_USER\" WHERE \"USER_ID\" = @ID AND \"USER_PW\" = @Password;";
                    cmd.Parameters.AddWithValue("ID", user_id);
                    cmd.Parameters.AddWithValue("Password", user_pw);

                    using (var reader = cmd.ExecuteReader())
                    {

                        if (!reader.HasRows)
                        {
                            // 일치하는 사용자가 없으면 false 반환
                            Console.WriteLine($"사용자가 없다");
                            return false;
                        }
                    }
                }

                // 모든 처리가 완료되면 true 반환
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine("fales");
                return false; // 예외 처리: 데이터베이스 오류가 발생한 경우 false 반환
            }
            finally
            {
                pgdb.Close(); // 데이터베이스 연결 닫기 (finally 블록은 항상 실행됨)
            }
        }
        // 아이디 중복
        public bool idrd_check(string input_id)
        {
            try
            {
                pgdb.Open(); // 데이터베이스 연결 열기
                using (NpgsqlCommand cmd = new NpgsqlCommand())
                {
                    cmd.Connection = pgdb;
                    cmd.CommandText = "SELECT * FROM public.\"TB_USER\" WHERE \"USER_ID\" = @ID;";
                    cmd.Parameters.AddWithValue("ID", input_id);

                    using (var reader = cmd.ExecuteReader())
                    {

                        if (!reader.HasRows)
                        {
                            // 일치하는 사용자가 없으면 true 반환
                            Console.WriteLine($"아이디 사용가능");
                            return true;
                        }
                    }
                }

                // 아이디가 존재하면 fales반환
                Console.WriteLine($"아이디 불가");
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine("fales");
                return false; // 예외 처리: 데이터베이스 오류가 발생한 경우 false 반환
            }
            finally
            {
                pgdb.Close(); // 데이터베이스 연결 닫기 (finally 블록은 항상 실행됨)
            }
        }
        // ATTITUDE
        public void attitude(int user_code, int att_code)
        {
            Console.WriteLine("수업태도 저장 확인");
            try
            {
                Console.WriteLine("수업태도 저장 확인");
                pgdb.Open(); // 데이터베이스 연결 열기
                using (NpgsqlCommand cmd = new NpgsqlCommand())
                {
                    cmd.CommandText = "INSERT INTO public.\"TB_ATTITUDE\" (\"USER_CODE\", \"ATTITUDE_CODE\", \"ATTITUDE_TIME\") " +
                                      "VALUES (@user_code, @att_code, @att_time);";
                    cmd.Parameters.AddWithValue("user_code", user_code);
                    cmd.Parameters.AddWithValue("att_code", att_code);
                    string att_time = timr_return();
                    cmd.Parameters.AddWithValue("att_time", att_time);
                    Console.WriteLine($"수업태도 저장 확인{att_time}");
                    cmd.ExecuteNonQuery(); // INSERT 쿼리 실행

                    //// 변경 사항 커밋
                    //pgdb.Commit();
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine("fales");
            }
            finally
            {
                pgdb.Close(); // 데이터베이스 연결 닫기 (finally 블록은 항상 실행됨)
            }
        }


        // 년,월,일 반환
        public string timr_return()
        {
            string formattedDate = DateTime.Now.ToString("yyyy-MM-dd");
            return formattedDate;
        }
    }
}

