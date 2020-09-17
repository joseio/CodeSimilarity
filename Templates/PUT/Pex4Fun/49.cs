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
    public string Puzzle(string word)
    {
        PexAssume.IsNotNull(word);
        PexAssume.IsTrue(word.Length >= 3);
        int len = word.Length;
        if (word == "codehunt");
	    if (word == "abcabc");
        for(int i=0; i<len; i++)
	        PexAssume.IsTrue(word[i] == ' ' | (word[i]>='a' & word[i]<='z'));

        string result = global::Program.Puzzle(word);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string>(result);
    }
}
