# Graph.canEvaluateGraph Method

Parent Object: [Graph](Graph.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Check if all the channels in the graph can be evaluated and in a good state.

## Syntax

"graph_var" is a variable referencing a [Graph](Graph.md) object.

```python
returnValue = graph_var.canEvaluateGraph()
```

## Return Value

| Type    | Description                                           |
|---------|-------------------------------------------------------|
| boolean | True if this graph can be evaluated, false otherwise. |

## Version

Introduced in version July 2025  

