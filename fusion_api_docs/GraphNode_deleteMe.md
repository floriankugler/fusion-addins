# GraphNode.deleteMe Method

Parent Object: [GraphNode](GraphNode.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Deletes the graphNode and all of its connections.

## Syntax

"graphNode_var" is a variable referencing a [GraphNode](GraphNode.md) object.

```python
returnValue = graphNode_var.deleteMe()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true in the case where the deletion was successful. All properties and proery objects of this node will become invalid after this call. Output nodes cannot be deleted. |

## Version

Introduced in version May 2025  

