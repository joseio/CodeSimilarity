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
    public string Puzzle(int lowerBound, int upperBound)
    {
        PexAssume.IsTrue(0 < lowerBound & lowerBound < 100);
        PexAssume.IsTrue(0 < upperBound & upperBound < 100);
        if ((lowerBound == 21 & upperBound == 6) | (lowerBound == 23 & upperBound == 14));

        int result = global::Program.Puzzle(lowerBound, upperBound);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int>(result);
    }
}
