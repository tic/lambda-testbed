from main import test, test_list
from utils import default_event

@test('exampleA', id=1)
def facilitiesApiTest():
    context = None
    event = default_event()

    # Write a function to evaluate whether the output was correct,
    # or pass a non-function value and it will check for equality.
    # Default equality checks are done with Python's default '=='
    def verifier(result):
        # @result is passed in directly through from the lambda.
        from json import dumps, loads
        if dumps(loads(result)) == dumps({"message": "Missing Authentication Token"}):
            return True
        else: return False
    return (event, context, verifier)
