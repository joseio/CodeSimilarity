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
    public string Puzzle(int[] a, int t)
    {
        PexAssume.IsNotNull(a);
        PexAssume.IsTrue(a.Length >= 2 & a.Length <= 5);
        foreach (int v in a) PexAssume.IsTrue(v >= -50 & v <= 50);
        PexAssume.IsTrue(t >= 1 & t <= 50);
        // 12/13/19: Commenting below line to see if it gets rid of FP in cluster 0
        // if (t == 10 || t == 20 || t == 30);

        int[] result = global::Program.Puzzle(a, t);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int[]>(result);
    }
}
