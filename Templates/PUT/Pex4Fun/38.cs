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
    public string Puzzle(int i, string s)
    {
        PexAssume.IsTrue(i >= 0 & i < 1000);
        PexAssume.IsNotNull(s);
        PexAssume.IsTrue(s.Length >= 3);
        int len = s.Length;
        if (s == "codehunt");
        if (s == "abcabc");
        for(int x=0; x<len; x++)
            PexAssume.IsTrue(s[x] == ' ' | (s[x]>='a' & s[x]<='z'));

        string result = global::Program.Puzzle(i, s);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string>(result);
    }
}
