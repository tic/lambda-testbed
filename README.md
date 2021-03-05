# Lambda Testbed
This repository contains a small framework which allows for easy testing of AWS style lambda functions written in Python 3.5+. It built for the [University of Virginia](https://virginia.edu/)'s [Development Hub](https://devhub.virginia.edu/) after multiple projects adopted development stacks involving AWS lambda functions and needed a more efficient testing method.

It presents a very simplistic interface and is designed to be easy to use for people of nearly all programming levels, ranging from novice to expert. If you like this framework or have found it useful for your project, leave a star so I know it was helpful!

### How do I use this testing framework?

1. Navigate to the [releases](https://github.com/tic/lambda-testbed/releases) section of the repo, select the latest one, download the `Source (zip)`, and extract to wherever you need it.
2. Drop your AWS style lambda functions into `/functions`.
3. Add test cases in `/tests.py` for your lambda functions.
4. Run `python main.py` from the root of the repository folder.
  - **Note:** The example file provided uses the `requests` Python package, but the framework does not require this package.
5. Sit back and relax while your tests are evaluated and results are printed to the screen!

## Documentation
### Adding your Lambda functions
Adding functions to the testbed is a simple drag-and-drop. In this repo, notice the `/functions` folder; anything can be put into this folder, but at the minimum it must contain all the lambda functions you wish to test. For the files containing lambda function code, they must follow this rule:
* The file must contain a function with this signature: `def lambda_function(event, context)`. Files which fail to implement this function in this way will either error out or be evaluated incorrectly.

This repo contains an example of this expected format. In `/functions/exampleA.py`, notice that there is an implementation of `lambda_function` exactly as described above. Depending on how your lambda functions are structured in AWS, you may be able to drop them directly into this folder without any extra work.

---
### Writing test cases
All test cases are written in `/tests.py`. This file may be modified to your heart's content, with the exception of the first import statement that is currently present. Without this import, tests will not be appropriately registered with the test conductor.

#### Adding a test case
In this testbed, there are two elements which are necessary to properly define a test case. All test cases are represented as functions which satisfy these requirements:
* The function is decorated by the `test` decorator.
* The function returns a tuple containing event, context, verifier objects.

To add your own, custom test cases, do the following for each desired test:
1. Define a new function (the name is not important so long as it doesn't share a name with any other test cases).
2. Decorate the function with the provided `test` decorator. You need to tell the decorator which file the test case is meant to test. If desired, you may specify `id` as a keyword argument to the decorator; this id is printed with test results to identify failures or successes.
3. In the function, generate the desired lambda inputs. This consists of event and context objects. `/utils.py` contains basic functions for creating a dummy context and basic events. Alternatively, you can create your own event and context objects.
4. Return a tuple of the form `(event, context, verifier)`. The verifier can be one of two things: something that represents the "correct answer" i.e. what the lambda is supposed to respond given the event and context you have created; or a function which accepts the lambda's result as an argument and determines correctness on its own. Further explanation of the verifier follows:

##### Using the built in result verifier
Some lambda functions return simple information that can be checked simply using `==`. If you return a non-callable object as the third element of the `(event, context, verifier)` tuple, this will be interpreted as the expected lambda result. After the lambda is evaluated, success of the test is determined via `result == verifier`. Consider this example:
```python
@test('myLambda', id=4)
def simpleTest():
	return (default_event(), default_context(), 59)
```
From this test case, we know the following:
* The lambda function this case is testing is contained in `/function/myLambda.py'
* Test results relating to this particuar test case will be tagged with and ID of 4.
* The lambda function is expected to return the number 59.

##### Using a custom result verifier
If your lambda requires more than a simple equality check to verify correctness, you may pass a function which will be used to determine whether the lambda's test was successful or not. The main idea with a custom verifier is that instead of doing the comparison `result == verifier` to check correctness, we do `verifier(result) == True`. In this case, `verifier` is a *callable* (i.e. a function) and is given the result of the lambda as its first and only argument. We can modify the previous example to use a custom verifying function:
```python
@test('myLambda', id=4)
def simpleTest():

	def check_result(result):
		if result == 59: return True
		else: return False

	return (default_event(), default_context(), check_result)
```
While this may appear more verbose than necessary in this particular example, many lambas will require that their correctness is evaluated in this fashion since the `==` operator may not work as expected with non-primitives (such as Python dicts).

---
### Running your tests
Once you have put all necessary files in place and written the various test cases, all you need to do is run `python main.py` from the root of the repo directory. The main script will load all of the test cases you have written, evaluate the lambda functions using the events and contexts your test cases generate, and display correctness results as determined by either the built in verifying function or the one you wrote in a given test case.

It's worth noting that test cases are fully insulated from one another. Anything you do in a particular test case should have no impact on the others, unless you are modifying built in Python things.

---

---

<sup>Written 02/19/21 by G. Michael Fitzgerald | You can find my website [here](https://gifit.io/)</sup>
<sup>This markdown file was tested using [pandao's](https://github.com/pandao) online [markdown editor](https://pandao.github.io/editor.md/en.html).</sup>
