using System;
using System.Collections.Generic;
using System.Text;
using System.Reflection;
using System.Reflection.Emit;

//using System.Reflection.Emit;

namespace StaticExampleLibrary
{
    public class StaticExampleLibrary
    {
        public static readonly String ROBOT_LIBRARY_SCOPE = "GLOBAL";

        public static readonly String ROBOT_LIBRARY_VERSION = "2.8.6";
        
        //public Action simple_keyword = _simple_keyword;

        //public Action<String> greet = _greet;

        //public Func<String> multiply_by_two(String number) = _multiply_by_two(String number);

//        public static readonly String NAME = "StaticExampleLibrary";

        public static void static_simple_keyword()
        {
            //"""Log a message"""
            System.Console.WriteLine("You have used the simplest <static> keyword.");
        }

        public void simple_keyword()
        {
            //"""Log a message"""
            System.Console.WriteLine("You have used the simple keyword.");
        }

        public static void greet(String name)
        {
            //   """Logs a friendly greeting to person given as argument"""
            System.Console.WriteLine("Hello " + name);
        }
        private static String _multiply_by_two(String number)
        {
            /*   """Returns the given number multiplied by two
   
               The result is always a floating point number.
               This keyword fails if the given `number` cannot be converted to number.
               """*/
            System.Console.WriteLine("*DEBUG* Got arguments " + number);
            return (float.Parse(number) * 2).ToString();
        }

        public static void numbers_should_be_equal(String first, String second)
        {
            System.Console.WriteLine("*DEBUG* Got arguments " + first + " and " + second);
            if (Convert.ToDouble(first) != Convert.ToDouble(second))
            {
                System.Console.WriteLine("*DEBUG* Exception");
                throw new Exception("Given numbers are unequal!");
            }
        }
    }
}
