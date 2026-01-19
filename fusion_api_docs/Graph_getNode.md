# Graph.getNode Method

Parent Object: [Graph](Graph.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get node with the given name.

## Syntax

"graph_var" is a variable referencing a [Graph](Graph.md) object.

```python
returnValue = graph_var.getNode(name)
```

## Return Value

| Type                       | Description                        |
|----------------------------|------------------------------------|
| [GraphNode](GraphNode.md) | The node if found, null otherwise. |

## Parameters

| Name | Type   | Description         |
|------|--------|---------------------|
| name | string | Name to search for. |

## Version

Introduced in version May 2025  

