using System;
using Microsoft.Pex.Framework;
using Microsoft.Pex.Framework.Validation;
using Microsoft.VisualStudio.TestTools.UnitTesting;

/// <summary>This class contains parameterized unit tests for Program</summary>
[PexClass(typeof(global::Program))]
[PexAllowedExceptionFromTypeUnderTest(typeof(InvalidOperationException))]
[PexAllowedExceptionFromTypeUnderTest(typeof(ArgumentException), AcceptExceptionSubtypes = true)]
[TestClass]
public partial class ProgramTest
{
    /// <summary>Test stub for Puzzle(Int32[])</summary>
    [PexMethod]
    public string Puzzle(string input, string a, string b, string c)
    {
        PexAssume.IsNotNull(input);
        PexAssume.IsNotNull(a);
        PexAssume.IsNotNull(b);
        PexAssume.IsNotNull(c);
        PexAssume.IsTrue(input.Length >= 3);
        PexAssume.IsTrue(a.Length >= 3);
        PexAssume.IsTrue(b.Length >= 3);
        PexAssume.IsTrue(c.Length >= 3);
        
        int lenInput = input.Length;
        if (input == "codehunt");
        if (input == "abcabc");
        for(int i=0; i<lenInput; i++)
            PexAssume.IsTrue(input[i] == ' ' | (input[i]>='a' & input[i]<='z'));

        int lenA = a.Length;
        if (a == "codehunt");
        if (a == "abcabc");
        for(int i=0; i<lenA; i++)
	        PexAssume.IsTrue(a[i] == ' ' | (a[i]>='a' & a[i]<='z'));
        
        int lenB = b.Length;
        if (b == "codehunt");
        if (b == "abcabc");
        for(int i=0; i<lenB; i++)
            PexAssume.IsTrue(b[i] == ' ' | (b[i]>='a' & b[i]<='z'));

        int lenC = c.Length;
        if (c == "codehunt");
        if (c == "abcabc");
        for(int i=0; i<lenC; i++)
            PexAssume.IsTrue(c[i] == ' ' | (c[i]>='a' & c[i]<='z'));

        bool result = global::Program.Puzzle(input, a, b, c);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<bool>(result);
    }
}
