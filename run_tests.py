import pytest



result = pytest.main([
    "tests",
    "-v",
    "--junitxml=results.xml"
])

print("Exit code:", result)
print("Tests completed.")