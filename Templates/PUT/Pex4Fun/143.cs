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
    public string Puzzle(string[] a)
    {
        PexAssume.IsNotNull(a);
        PexAssume.IsTrue(a.Length >= 2 & a.Length <= 5);
        foreach (var v in a)
        {
            PexAssume.IsNotNull(v);
            PexAssume.IsTrue(v.Length >= 3);
            for (int i = 0; i < v.Length; i++)
                PexAssume.IsTrue(v[i] == ' ' | (v[i] >= 'a' & v[i] <= 'z'));
        }

        string[] result = global::Program.Puzzle(a);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string[]>(result);
    }
}
