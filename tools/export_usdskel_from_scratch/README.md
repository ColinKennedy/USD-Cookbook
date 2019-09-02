This Python package exports an animated skeleton (with a skinned mesh)
to disk. It's a basic implementation of a UsdSkel exporter. That said,
it's mainly for learning purposes and to see how Maya and USD fit
together during exporting. This tool will be helpful to 2 types of
people:

- Someone looking to understand how UsdSkel works with a practical example
- Someone who cannot use USD's pre-existing Maya exporter plugin and
  have to actually write the UsdSkel export process from scratch

If you fall under either camp then you will get a lot out of trying
this tool out. But if you aren't learning UsdSkel or aren't expected to
re-write an exporter, feel free to skip this project.


## Maya Scene Requirements
- The DAG graph needs to looks like this
    - root (Group node)
	    - joints (Joint node)
		    - joints1
		    - joints2
		    - joints3
		    - jointsEtc
		- geometry (Group node)
		    - mesh1
		    - mesh2
		    - mesh3
		    - meshEtc
    - The top-most group that has both the joints and meshes is used as the UsdSkelRoot


There's an example scene file located at
[example/joints.ma](example/joints.ma) which already has this set up.


## To run
1. Load Maya. (__Important__: This assumes that [Maya's USD plugin is installed correctly](https://graphics.pixar.com/usd/docs/Maya-USD-Plugins.html))

```sh
PYTHONPATH=$PWD/python:$USD_INSTALL_ROOT/python:$PYTHONPATH maya
```

2. Open [example/joints.ma](example/joints.ma) to get a scene with
   joints + a bound mesh or create your own

3. Run this Python code:

```python
from convert_maya_to_usdskel import converter

node = 'root_joint'
converter.write_rig_as_usdskel(
    node, 
    "/SkeletonRoot",
    "/SkeletonAnimation",
    "/tmp/test_export",
)
```


## Disclaimers
This script exports a skeleton definition and animation in a single
export command.

In a real pipeline, the command would be split into 2 parts:
- A rigger would export the skeleton
- An animator would export just the animation

This script exports in a single step to keep the code simple. But most
likely, when exporting an animation, you would link to a USD file for
the skeleton that already has been written to disk.

- Generally speaking, only a basic skeleton could be exported like this.
    - Joints with offset groups aren't respected (as well as other more
	complex rigging features)


## References
https://toolchefs.atlassian.net/wiki/spaces/ASD/blog/2018/09/03/198737921/Atoms+Cache+To+USD

https://www.youtube.com/watch?v=ECS-ntgnf24

https://atoms.toolchefs.com/

https://github.com/meshula/usdskelutil
