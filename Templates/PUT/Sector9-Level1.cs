using System;
using Microsoft.Pex.Framework;
using System.Collections.Generic;
using Microsoft.Pex.Framework.Validation;
using Microsoft.VisualStudio.TestTools.UnitTesting;

/// <summary>This class contains parameterized unit tests for Program</summary>
//[PexClass(typeof(global::Program), MaxRuns = 1)]
[PexAllowedExceptionFromTypeUnderTest(typeof(InvalidOperationException))]
[PexAllowedExceptionFromTypeUnderTest(typeof(ArgumentException), AcceptExceptionSubtypes = true)]
[TestClass]
public partial class ProgramTest
{
    /// <summary>Test stub for Sort(Int32[])</summary>
    [PexMethod(MaxBranches = 100000, MaxConditions = 4000)]
    public string Sort(int[] a)
    {
        // PexAssume.IsTrue(x >= 0 & x < 1000);
        PexAssume.IsNotNull(a);
        PexAssume.IsTrue(a.Length >= 2 & a.Length <= 4);
        foreach (int v in a) PexAssume.IsTrue(v >= -10 & v <= 10);
        
        int[] result = global::Program.Sort(a);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int[]>(result);
    }
}