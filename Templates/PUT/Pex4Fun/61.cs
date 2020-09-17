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
    public string Puzzle(int i, int j, int k)
    {
        PexAssume.IsTrue(0 < i & i < 100);
        PexAssume.IsTrue(0 < j & j < 100);
        PexAssume.IsTrue(0 < k & k < 100);
        if ((i == 21 & j == 6 & k == 11) | (i == 23 & j == 14 & k == 20));

        string result = global::Program.Puzzle(i, j, k);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string>(result);
    }
}
