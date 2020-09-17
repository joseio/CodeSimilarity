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
    public string Puzzle(int slope1, int yintercept1, int slope2)
    {
        PexAssume.IsTrue(0 < slope1 & slope1 < 100);
        PexAssume.IsTrue(0 < yintercept1 & yintercept1 < 100);
        PexAssume.IsTrue(0 < slope2 & slope2 < 100);
        PexAssume.IsTrue(0 < yintercept2 & yintercept2 < 100);
        if ((slope1 == 21 & yintercept1 == 6 & slope2 == 11 & yintercept2 = 14) | (slope1 == 23 & yintercept1 == 14 & slope2 == 20 & yintercept2 = 18));

        string result = global::Program.Puzzle(slope1, yintercept1, slope2, yintercept2);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string>(result);
    }
}
