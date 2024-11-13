# Jacro

Think "xacro" but with Jinja - we just swapped the "x" for "j". Not the most creative naming! 🤷 Just a small wrapper around [jinja2](https://jinja.palletsprojects.com/en/stable/) - if you're not using ROS 2, you probably want to use jinja2 directly!

[![Build Status](https://github.com/JafarAbdi/jacro/actions/workflows/build_and_test.yaml/badge.svg)](https://github.com/JafarAbdi/jacro/actions/workflows/build_and_test.yaml)

## Usage

```python
import jacro

jacro.process_text("Text {{ arg1 }}/{{ arg2 }}", mappings={"arg1": "value1", "arg2": "value2"})
jacro.process_file("filename.ext", mappings={"arg1": "value1", "arg2": "value2"})
```

You can use all functionality from jinja2 (even as a replacement to xacro itself!)

### Custom functions

Currently, jacro have the following extra registered functions:

- `ros_pkg_path('pkg')`: Will be replaces with the shared directory of 'pkg'

```
urdf: {{ ros_pkg_path('my_robot_description') }} -> urdf: /path/to/my_robot_description/share/my_robot_description
urdf: {{ ros_pkg_path('std_msgs') }} -> urdf: /opt/ros/humble/share/std_msgs
```

## Command-Line Interface

To save the output to a file, use the `-o` or `--output` option.

```bash
jacro input_filename -o output_filename arg1=value1 arg2=value2 ...
```

To print the output to the console

```bash
jacro input_filename arg1:=value_1 arg2:=[1, 2, 3] arg3:=["asd", "jafar"] ...
```

## Linting

Using pre-commit

```bash
pre-commit run -a
```

## Testing

Using pytest directly

```bash
python -m pytest --capture=no
```

Or using colcon

```bash
colcon build --packages-up-to jacro
colcon test --packages-select jacro
colcon test-result
```
