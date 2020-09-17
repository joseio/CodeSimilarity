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
    public string Puzzle(int a, int b, int c)
    {
        PexAssume.IsTrue(0 < a & a < 100);
        PexAssume.IsTrue(0 < b & b < 100);
        PexAssume.IsTrue(0 < c & c < 100);
        if ((a == 21 & b == 6 & c == 11) | (a == 23 & b == 14 & c == 20));

        bool result = global::Program.Puzzle(a, b, c);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<bool>(result);
    }
}
