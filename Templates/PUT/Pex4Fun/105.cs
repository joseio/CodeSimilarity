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
    public string Puzzle(int[] list, int i)
    {
        PexAssume.IsNotNull(list);
        PexAssume.IsTrue(list.Length >= 2 & list.Length <= 5);
        foreach (int v in list) PexAssume.IsTrue(v >= -50 & v <= 50);
        PexAssume.IsTrue(i >= 1 & i <= 50);
        // 12/13/19: Commenting below line to see if it gets rid of FP in cluster 0
        // if (i == 10 || i == 20 || i == 30);

        bool result = global::Program.Puzzle(list, i);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<bool>(result);
    }
}
