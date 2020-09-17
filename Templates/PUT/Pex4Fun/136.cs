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
    public string Puzzle(int[] numbers, int x)
    {
        PexAssume.IsNotNull(numbers);
        PexAssume.IsTrue(numbers.Length >= 2 & numbers.Length <= 5);
        foreach (int v in numbers) PexAssume.IsTrue(v >= -50 & v <= 50);
        PexAssume.IsTrue(x >= 1 & x <= 50);
        // 12/13/19: Commenting below line to see if it gets rid of FP in cluster 0
        // if (x == 10 || x == 20 || x == 30);

        int[] result = global::Program.Puzzle(numbers, x);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int[]>(result);
    }
}
