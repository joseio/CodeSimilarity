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
     public string Puzzle(int[] a, int k) {
     	PexAssume.IsNotNull(a);
	    PexAssume.IsTrue(a.Length >= 4 & k >= 0 & k < a.Length);
		foreach(int v in a) PexAssume.IsTrue(v>=-100 & v<=100);

		int result = global::Program.Puzzle(a, k);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int>(result);
     }
}