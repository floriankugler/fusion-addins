# Graph.disconnect Method

Parent Object: [Graph](Graph.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Delete a connection between nodes.

## Syntax

"graph_var" is a variable referencing a [Graph](Graph.md) object.

```python
returnValue = graph_var.disconnect(outputNode, outputPinIndex, inputNode, inputPinIndex)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| outputNode | [GraphNode](GraphNode.md) | The node where the connection starts. |
| outputPinIndex | uinteger | The index of the output pin on the start node. |
| inputNode | [GraphNode](GraphNode.md) | The node where the connection ends. |
| inputPinIndex | uinteger | The index of the input pin on the end node. |

## Version

Introduced in version May 2025  

