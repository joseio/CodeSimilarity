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
    public string Puzzle(string a, string b)
    {
        PexAssume.IsNotNull(a);
        PexAssume.IsNotNull(b);
        PexAssume.IsTrue(a.Length >= 3);
        PexAssume.IsTrue(b.Length >= 3);
        
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

        int result = global::Program.Puzzle(a, b);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int>(result);
    }
}
