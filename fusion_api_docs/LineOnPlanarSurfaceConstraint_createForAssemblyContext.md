# LineOnPlanarSurfaceConstraint.createForAssemblyContext Method

Parent Object: [LineOnPlanarSurfaceConstraint](LineOnPlanarSurfaceConstraint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"lineOnPlanarSurfaceConstraint_var" is a variable referencing a [LineOnPlanarSurfaceConstraint](LineOnPlanarSurfaceConstraint.md) object.

```python
returnValue = lineOnPlanarSurfaceConstraint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [LineOnPlanarSurfaceConstraint](LineOnPlanarSurfaceConstraint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2023  

