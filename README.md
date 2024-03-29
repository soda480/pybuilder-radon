# pybuilder-radon
[![GitHub Workflow Status](https://github.com/soda480/pybuilder-radon/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-radon/actions)
[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://pybuilder.io/)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![PyPI version](https://badge.fury.io/py/pybuilder-radon.svg)](https://badge.fury.io/py/pybuilder-radon)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)

A pybuilder plugin that checks the cyclomatic complexity of your project using `radon`. For more information about radon refer to the [radon pypi page](https://pypi.org/project/radon/).

To add this plugin into your pybuilder project, add the following line near the top of your build.py:
```python
use_plugin('pypi:pybuilder_radon')
```

**NOTE** if you are using Pybuilder version `v0.11.x`, then specify the following version of the plugin:
```python
use_plugin('pypi:pybuilder_radon', '~=0.1.2')
```

### cyclomatic complexity

Cyclomatic complexity is a software metric used to indicate the complexity of a program. It is a quantitative measure of the number of linearly independent paths through a program's source code. Cyclomatic complexity can be used to measure code complexity. The higher the complexity score the more complex the code, which typically translates to the code being more difficult to understand, maintain and to test. The number of the Cyclomatic complexity depends on how many different execution paths or control flow of your code can execute depending on various inputs. The metrics for Cyclomatic Complexity are:

Score | Complexity | Risk Type
-- | -- | --
1 to 10 | simple | not much risk
11 to 20 | complex | low risk
21 to 50 | too complex | medium risk, attention
more than 50 | very complex | unable to test, high risk

Refer to [cyclomatic complexity](https://www.c-sharpcorner.com/article/code-metrics-cyclomatic-complexity/) for more information.

### Pybuilder radon properties

The pybuilder task `pyb radon` will use radon to to analyze your project and display the average cyclomatic complexity, verbose mode will display complexity of all classes, functions and methods analyzed. The following plugin properties are available to further configure the plugin's execution.

Name | Type | Default Value | Description
-- | -- | -- | --
radon_break_build_average_complexity_threshold | float | None | Fail build if overall average complexity is greater than the specified threshold
radon_break_build_complexity_threshold | float | None | Fail build if complexity of any class, function or method exceeds the specified threshold

The plugin properties are set using `project.set_property`, for example setting the following properties, `pyb complexity` will fail if the average overall complexity score of the project exceeds `4` or if the complexity score of **any** class, method or function exceeds `10`:

```Python
project.set_property('radon_break_build_average_complexity_threshold', 4)
project.set_property('radon_break_build_complexity_threshold', 10)
```

### Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t pybradon:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/code \
pybradon:latest \
bash
```

Execute the build:
```sh
pyb -X
```
