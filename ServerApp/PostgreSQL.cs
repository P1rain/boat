using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using Npgsql;

namespace ConsoleApp1
{
    class Postgresql
    {
        public bool ConnectionTest()
        {
            string connectString = string.Format("Host={0};Database={1};Username ={2};Password={3};", "10.10.20.114", "pirates", "postgres", "ilsan1236526");
            try
            {
                using (NpgsqlConnection conn = new NpgsqlConnection(connectString))
                {
                    conn.Open();
                }
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public void SelectDB()
        {
            string connectString = string.Format("Host={0};Database={1};Username ={2};Password={3};", "10.10.20.114", "pirates", "postgres", "ilsan1236526");
            string sql = "select * from TB_ATTEND_LECTURE";

            using (NpgsqlConnection conn = new NpgsqlConnection(connectString))
            {
                conn.Open();

                NpgsqlCommand cmd = new NpgsqlCommand(sql, conn);
                NpgsqlDataReader dr = cmd.ExecuteReader();
                dr.Close();
            }
        }
        public void InsertDB(int id, string name)
        {
            string connectString = string.Format("Host={0};Database={1};Username ={2};Password={3};", "10.10.20.114", "pirates", "postgres", "ilsan1236526");
            string sql = $"Insert Into UserInfo  (id,name) values ({id},'{name}')";

            using (NpgsqlConnection conn = new NpgsqlConnection(connectString))
            {
                conn.Open();
                NpgsqlCommand cmd = new NpgsqlCommand(sql, conn);
                cmd.ExecuteNonQuery();
            }
        }
        public DataSet GetUserInfo()
        {
            string connectString = string.Format("Host={0};Database={1};Username ={2};Password={3};", "10.10.20.114", "pirates", "postgres", "ilsan1236526");
            string sql = "select * from UserInfo";
            DataSet ds = new DataSet();

            using (NpgsqlConnection conn = new NpgsqlConnection(connectString))
            {
                conn.Open();
                NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, conn);
                da.TableMappings.Add("UserInfo", "1");
                da.Fill(ds);
            }
            return ds;
        }
    }
}
