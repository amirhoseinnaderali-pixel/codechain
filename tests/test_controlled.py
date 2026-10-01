from scripts.run_controlled import extract_code, run_code


def test_extract_code():
    fence = chr(96) * 3
    source = fence + "python\nprint(1)\n" + fence
    assert extract_code(source) == "print(1)"


def test_run_code():
    result = run_code("x = int(input())\nprint(x + 1)", "4\n", timeout=2)
    assert result["passed_process"]
    assert result["stdout"].strip() == "5"
