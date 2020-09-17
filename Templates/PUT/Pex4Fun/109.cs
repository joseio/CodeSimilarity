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
    public string Puzzle(string s)
    {
        PexAssume.IsNotNull(s);
        PexAssume.IsTrue(s.Length >= 3);
        int len = s.Length;
        if (s == "codehunt");
	    if (s == "abcabc");
        for(int i=0; i<len; i++)
	        PexAssume.IsTrue(s[i] == ' ' | (s[i]>='a' & s[i]<='z'));

        string[] result = global::Program.Puzzle(s);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string[]>(result);
    }
}
