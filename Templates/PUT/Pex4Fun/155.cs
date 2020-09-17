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
    public string Puzzle(int x)
    {
        PexAssume.IsTrue(x >= 0 & x < 1000);

        int result = global::Program.Puzzle(x);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int>(result);
    }
}
