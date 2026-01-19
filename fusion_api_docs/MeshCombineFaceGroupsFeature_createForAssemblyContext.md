# MeshCombineFaceGroupsFeature.createForAssemblyContext Method

Parent Object: [MeshCombineFaceGroupsFeature](MeshCombineFaceGroupsFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"meshCombineFaceGroupsFeature_var" is a variable referencing a [MeshCombineFaceGroupsFeature](MeshCombineFaceGroupsFeature.md) object.

```python
returnValue = meshCombineFaceGroupsFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [MeshCombineFaceGroupsFeature](MeshCombineFaceGroupsFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2025  

