using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace YourNamespace
{
    public class User
    {
        public int user_code { get; set; } = 0;
        public string user_id { get; set; } = string.Empty;
        public string user_pw { get; set; } = string.Empty;
        public string user_name { get; set; } = string.Empty;
        public string user_parent { get; set; } = string.Empty;

        public override string ToString()
        {
            return $"{this.ToJsonAnObject()}";
        }

        public Dictionary<string, object> ToJsonAnObject()
        {
            var objDict = new Dictionary<string, object>
            {
                { "user_code", this.user_code },
                { "user_id", this.user_id },
                { "user_pw", this.user_pw },
                { "user_name", this.user_name },
                { "user_parent", this.user_parent }
            };
            return objDict;
        }

        public override bool Equals(object obj)
        {
            if (obj is User other &&
                this.user_code == other.user_code &&
                this.user_id == other.user_id &&
                this.user_pw == other.user_pw &&
                this.user_name == other.user_name &&
                this.user_parent == other.user_parent)
            {
                return true;
            }
            return false;
        }
    }

    public class Attitude
    {
        public int user_code { get; set; }
        public int attitude_code { get; set; }
        public DateTime attitude_time { get; set; }

        public override string ToString()
        {
            return $"{this.ToJsonAnObject()}";
        }

        public Dictionary<string, object> ToJsonAnObject()
        {
            var objDict = new Dictionary<string, object>
            {
                { "user_code", this.user_code },
                { "attitude_code", this.attitude_code },
                { "attitude_time", this.attitude_time }
            };
            return objDict;
        }

        public override bool Equals(object obj)
        {
            if (obj is Attitude other &&
                this.user_code == other.user_code &&
                this.attitude_code == other.attitude_code &&
                this.attitude_time == other.attitude_time)
            {
                return true;
            }
            return false;
        }
    }

    public class Lecture
    {
        public int lecture_code { get; set; }
        public DateTime lectured_time { get; set; }

        public override string ToString()
        {
            return $"{this.ToJsonAnObject()}";
        }

        public Dictionary<string, object> ToJsonAnObject()
        {
            var objDict = new Dictionary<string, object>
            {
                { "lecture_code", this.lecture_code },
                { "lectured_time", this.lectured_time }
            };
            return objDict;
        }

        public override bool Equals(object obj)
        {
            if (obj is Lecture other &&
                this.lecture_code == other.lecture_code &&
                this.lectured_time == other.lectured_time)
            {
                return true;
            }
            return false;
        }
    }

    public class AttendLecture
    {
        public int user_code { get; set; }
        public int lecture_code { get; set; }
        public DateTime attend_time { get; set; }
        public string complete_status { get; set; }

        public override string ToString()
        {
            return $"{this.ToJsonAnObject()}";
        }

        public Dictionary<string, object> ToJsonAnObject()
        {
            var objDict = new Dictionary<string, object>
            {
                { "user_code", this.user_code },
                { "lecture_code", this.lecture_code },
                { "attend_time", this.attend_time },
                { "complete_status", this.complete_status }
            };
            return objDict;
        }

        public override bool Equals(object obj)
        {
            if (obj is AttendLecture other &&
                this.user_code == other.user_code &&
                this.lecture_code == other.lecture_code &&
                this.attend_time == other.attend_time &&
                this.complete_status == other.complete_status)
            {
                return true;
            }
            return false;
        }
    }

    public class ObjEncoder
    {
        public static ObjEncoder Instance { get; } = new ObjEncoder();

        private ObjEncoder() { }

        public string ToJsonAsBinary(object obj)
        {
            if (obj is List<object> list)
            {
                var temp_list = new List<string>();
                foreach (var o in list)
                {
                    var str_obj = ToJsonAnObject(o);
                    temp_list.Add(str_obj);
                }
                var list_json = JsonSerializer.Serialize(temp_list);
                return list_json;
            }
            return ToJsonAnObjectWithEncode(obj);
        }

        public string ToJsonAnObjectWithEncode(object obj)
        {
            var json_string = ToJsonAnObject(obj);
            return json_string;
        }

        public string ToJsonAnObject(object obj)
        {
            Console.WriteLine(JsonSerializer.Serialize(obj));
            var json_string = JsonSerializer.Serialize(obj);
            return json_string;
        }
    }

    public class ObjDecoder
    {
        public static ObjDecoder Instance { get; } = new ObjDecoder();

        public ObjDecoder() { }

        public object BinaryToObj(byte[] binaryStr)
        {
            var binary_string = System.Text.Encoding.UTF8.GetString(binaryStr);
            return JsonToObject(binary_string);
        }

        public object BinaryToObj(string binaryStr)
        {
            return JsonToObject(binaryStr);
        }

        public object JsonToObject(string json)
        {
            var dictObj = JsonSerializer.Deserialize<Dictionary<string, object>>(json);

            if (dictObj.ContainsKey("user_id"))
            {
                return JsonSerializer.Deserialize<User>(json);
            }
            else if (dictObj.ContainsKey("complete_status"))
            {
                return JsonSerializer.Deserialize<AttendLecture>(json);
            }
            else if (dictObj.ContainsKey("attitude_time"))
            {
                return JsonSerializer.Deserialize<Attitude>(json);
            }
            else if (dictObj.ContainsKey("lectured_time"))
            {
                return JsonSerializer.Deserialize<Lecture>(json);
            }
            return dictObj;
        }

        public List<object> ListMapper(List<string> listObj)
        {
            var result_list = new List<object>();
            foreach (var o in listObj)
            {
                var converted_o = JsonToObject(o);
                result_list.Add(converted_o);
            }
            return result_list;
        }
    }
}
