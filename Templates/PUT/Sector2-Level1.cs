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
    public string Puzzle(int[] a)
    {
        PexAssume.IsNotNull(a);
        PexAssume.IsTrue(a.Length > 0);
        if (a.Length==3 && (a[0]==13 & a[1]==-5 && a[2]==7));
        foreach (var n in a) {
            PexAssume.IsTrue(n>=-100 & n<=100);
        }
        int result = global::Program.Puzzle(a);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int>(result);
    }
}
