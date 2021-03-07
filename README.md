[![GitHub Workflow Status](https://github.com/soda480/pybuilder-radon/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-radon/actions)
[![Code Coverage](https://codecov.io/gh/soda480/pybuilder-radon/branch/main/graph/badge.svg)](https://codecov.io/gh/soda480/pybuilder-radon)
[![Code Grade](https://www.code-inspector.com/project/19887/status/svg)](https://frontend.code-inspector.com/project/19887/dashboard)
[![PyPI version](https://badge.fury.io/py/pybuilder-radon.svg)](https://badge.fury.io/py/pybuilder-radon)

# pybuilder-radon #

A pybuilder plugin that computes the cyclomatic complexity of your project using `radon`. For more information refer to the [radon home page](https://pypi.org/project/radon/). To add this plugin into your pybuilder project, add the following line at the top of your build.py:
```python
use_plugin('pypi:pybuilder_radon', '~=0.1.0')
```

**NOTE** This version of the plugin only works with version `v0.11.x` of Pybuilder.

### cyclomatic complexity ###

Cyclomatic complexity is a software metric used to indicate the complexity of a program. It is a quantitative measure of the number of linearly independent paths through a program's source code. Cyclomatic complexity can be used to measure the code complexity. The higher the complexity, the more complex the code which typically means the code is more difficult to test and maintain. The number of the Cyclomatic complexity depends on how many different execution paths or control flow of your code can execute depending on various inputs. Refer to [cyclomatic complexity](https://www.c-sharpcorner.com/article/code-metrics-cyclomatic-complexity/) for more information. The metrics for Cyclomatic Complexity are:

Score | Complexity | Risk Type
-- | -- | --
1 to 10 | simple | not much risk
11 to 20 | complex | low risk
21 to 50 | too complex | medium risk, attention
more than 50 | very complex | unable to test, high risk


The pybuilder task `complexity` will use radon to to analyze your project and display the overall average cyclomatic complexity, verbose mode will display complexity of all classes, functions and methods analyzed. A few pybuilder properties can be set to fail the build if a complexity threshold has been exceeded.

### Pybuilder radon properties ###
Name | Type | Default Value | Description
-- | -- | -- | --
radon_break_build_average_complexity_threshold | float | None | Fail build if overall average complexity is greater than the specified threshold
radon_break_build_complexity_threshold | float | None | Fail build if complexity of any class, function or method exceeds the specified threshold


### Development ###

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t \
pybradon:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/pybuilder-radon \
pybradon:latest \
/bin/sh
```

Execute the build:
```sh
pyb -X
```