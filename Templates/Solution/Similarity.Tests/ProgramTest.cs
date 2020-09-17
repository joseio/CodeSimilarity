/*

// <copyright file="ProgramTest.cs">Copyright ©  2019</copyright>
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
    //[PexArguments(new int[] {48, 49, 50, 50, 50, 50, 50, 0, 15, 15, 15, 15, 15, 16, 50, 18, 18, 18, 18, 18})]
        public string Puzzle(int[] a)
    {
        //int result = global::Program.Puzzle(a);
        //return result;
        // TODO: add assertions to method ProgramTest.Puzzle(Int32[])
        PexAssume.IsNotNull(a);
        PexAssume.IsTrue(a.Length >= 2 & a.Length <= 20);
        foreach (int v in a) PexAssume.IsTrue(v >= -50 & v <= 50);

        int result = global::Program.Puzzle(a);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString(result);
    }
}
*/

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
    public string Puzzle(int[] a, int[] b)
    {
        PexAssume.IsNotNull(a);
        PexAssume.IsNotNull(b);
        PexAssume.IsTrue(a.Length >= 0 & a.Length <= 10);
        PexAssume.IsTrue(b.Length >= 0 & b.Length <= 10);
        foreach (int v in a) PexAssume.IsTrue(v >= 0 & v <= 255);
        foreach (int v in b) PexAssume.IsTrue(v >= 0 & v <= 255);

        int[] result = global::Program.Puzzle(a, b);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int[]>(result);
    }
}