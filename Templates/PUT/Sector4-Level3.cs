using System;
using System.Linq;
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
    public string Puzzle(int[] a, int[] b) {
        PexAssume.IsNotNull(a);
        PexAssume.IsNotNull(b);
        PexAssume.IsTrue(a.Length == 5);
        foreach (int v in a) PexAssume.IsTrue(v >= 0 & v <= 10);
        int max = a.Max();  
        PexAssume.IsTrue(b.Length > max);
        foreach (int v in b) PexAssume.IsTrue(v >= 0 & v <= 10);

        int[] result = global::Program.Puzzle(a, b);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int[]>(result);
    }
}