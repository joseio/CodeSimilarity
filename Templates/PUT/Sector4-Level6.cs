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
	public string Puzzle(string s) {
		PexAssume.IsNotNull(s);
	    if (s == "hello");
	    if (s == "thisisacodehuntpuzzle");
	    for (int i = 0; i < s.Length; i++) PexAssume.IsTrue('a' <= s[i] & s[i] <= 'z');

	    string result = global::Program.Puzzle(s);
        return PexSymbolicValue.GetPathConditionString() + " RET_DIV " + PexSymbolicValue.ToString<string>(result);
	}
}