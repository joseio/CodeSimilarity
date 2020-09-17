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
    public string Puzzle(int in_1, string in_2, int in_3)
    {
        PexAssume.IsTrue(in_1 > 1 & in_1 <= 50);
        PexAssume.IsTrue(in_3 > 1 & in_3 <= 50);
         // 12/13/19: Commenting below line to see if it gets rid of FP in cluster 0
        // if (in_1 == 10 || in_1 == 20 || in_1 == 30);

        PexAssume.IsNotNull(in_2);
        PexAssume.IsTrue(in_2.Length >= 3);
        int len = in_2.Length;
        if (in_2 == "codehunt");
        if (in_2 == "abcabc");
        for(int x=0; x<len; x++)
            PexAssume.IsTrue(in_2[x]>='a' & in_2[x]<='z');
       

        string result = global::GlobalMembers.Main(in_1, in_2, in_3);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string>(result);
    }
}
