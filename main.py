
test_list = []
def test(file, id=None):
    def decorate(func):
        test_list.append((file, func, str(id)))
        return func
    return decorate

def main():
    from tests import test_list
    import importlib.util
    functions = {}

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
            result = lambda_function(event, context)
        except Exception as err:
            print(f'[ERR] Encountered error in lamba function during test {test_func.__name__}#{id}:')
            print(err)
            continue

        try:
            if callable(verifier):
                if verifier(result):
                    print(f'[PASS] passed test {test_func.__name__}#{id}')
                else:
                    print(f'[FAIL] failed test {test_func.__name__}#{id}')
            else:
                if result == verifier:
                    print(f'[PASS] passed test {test_func.__name__}#{id}')
                else:
                    print(f'[FAIL] failed test {test_func.__name__}#{id}')
        except Exception as err:
            print(f'[ERR] Encountered error in result verifier for test {test_func.__name__}#{id}:')
            print(err)

if __name__ == '__main__':
    main()
