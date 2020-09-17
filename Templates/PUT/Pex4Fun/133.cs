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
    public string Puzzle(string[] words, string s)
    {
        PexAssume.IsNotNull(words);
        PexAssume.IsTrue(words.Length >= 2 & words.Length <= 5);
        PexAssume.IsNotNull(s);
        PexAssume.IsTrue(s.Length >= 3);

        foreach (var v in words)
        {
            PexAssume.IsNotNull(v);
            PexAssume.IsTrue(v.Length >= 3);
            for (int i = 0; i < v.Length; i++)
                PexAssume.IsTrue(v[i] == ' ' | (v[i] >= 'a' & v[i] <= 'z'));
        }
        
        int len = s.Length;
        if (s == "codehunt");
        if (s == "abcabc");
        for(int i=0; i<len; i++)
            PexAssume.IsTrue(s[i] == ' ' | (s[i]>='a' & s[i]<='z'));

        int result = global::Program.Puzzle(words, s);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<int>(result);
    }
}
