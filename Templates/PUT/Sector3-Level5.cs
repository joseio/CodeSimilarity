using System;
using Microsoft.Pex.Framework;
using Microsoft.Pex.Framework.Settings;
using Microsoft.Pex.Framework.Validation;
using Microsoft.VisualStudio.TestTools.UnitTesting;

/// <summary>This class contains parameterized unit tests for Program</summary>
[PexClass(typeof(global::Program))]
[PexAllowedExceptionFromTypeUnderTest(typeof(InvalidOperationException))]
[PexAllowedExceptionFromTypeUnderTest(typeof(ArgumentException), AcceptExceptionSubtypes = true)]
[TestClass]
public partial class ProgramTest
{
    [PexMethod]
	public int[][] Puzzle(int x, int y) {
        PexAssume.IsTrue(1<=x & x<=8 & 1<=y & y<=8);
        if (x==5&y==1 | x==3&y==8);  // Hint to user

    	int[][] result = global::Program.Puzzle(x, y);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int[][]>(result);
	}
}