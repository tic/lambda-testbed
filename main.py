
test_list = []
def test(file, id=None):
    def decorate(user_test_func):
        test_list.append((file, user_test_func, str(id)))
        return user_test_func
    return decorate

def main():
    from datetime import datetime
    from tests import test_list
    import importlib.util
    functions = {}
    passed = 0

    timesToSec = lambda start, stop : round((stop - start).microseconds / 10000) / 100

    test_start = datetime.now()
    for (file, test_func, id) in test_list:
        try:
            lamba_function = functions[file]
        except KeyError:
            spec = importlib.util.spec_from_file_location('user_tests', f'./functions/{file}.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            lambda_function = module.lambda_function
            functions[file] = lambda_function

        event, context, verifier = test_func()
        try:
            start = datetime.now()
            result = lambda_function(event, context)
            stop = datetime.now()
            execution_time = (stop - start).microseconds
        except Exception as err:
            print(f'[ERR] Encountered error in lamba function during test {test_func.__name__}#{id}:')
            print(err)
            continue

        try:
            time_passed = f'{execution_time} µs' if execution_time < 100000 else f'{timesToSec(start, stop)} s'

            did_pass = verifier(result) if callable(verifier) else result == verifier
            if did_pass:
                print(f'[PASS] passed test {test_func.__name__}#{id} ({time_passed})')
                passed += 1
            else:
                print(f'[FAIL] failed test {test_func.__name__}#{id} ({time_passed})')
        except Exception as err:
            print(f'[ERR] Encountered error in result verifier for test {test_func.__name__}#{id}:')
            print(err)

    test_stop = datetime.now()
    print(f'\n\nPassed {passed} of {len(test_list)} tests. ({timesToSec(test_start, test_stop)} s)')

if __name__ == '__main__':
    main()
