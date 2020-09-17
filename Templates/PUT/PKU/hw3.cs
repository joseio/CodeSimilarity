using System;
using Microsoft.Pex.Framework;
using Microsoft.Pex.Framework.Validation;
using Microsoft.VisualStudio.TestTools.UnitTesting;

/// <summary>This class contains parameterized unit tests for Program</summary>
[PexClass(typeof(global::GlobalMembers))]
[PexAllowedExceptionFromTypeUnderTest(typeof(InvalidOperationException))]
[PexAllowedExceptionFromTypeUnderTest(typeof(ArgumentException), AcceptExceptionSubtypes = true)]
[TestClass]
public partial class ProgramTest
{
    /// <summary>Test stub for Puzzle(Int32[])</summary>
    [PexMethod]
    public string Puzzle(int loop_len, double[] loop_input)
    {
        PexAssume.IsNotNull(loop_input);
        PexAssume.IsTrue(loop_input.Length >= 2 & loop_input.Length <= 5);
        PexAssume.IsTrue(loop_len >= 1 & loop_len < loop_input.Length);
        foreach (double v in loop_input) PexAssume.IsTrue(v >= -50 & v <= 50);
        // 12/13/19: Commenting below line to see if it gets rid of FP in cluster 0
        // if (loop_len == 10 || loop_len == 20 || loop_len == 30);

        double result = global::GlobalMembers.Main(loop_len, loop_input);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<double>(result);
    }
}
