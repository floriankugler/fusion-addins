# PerpendicularToSurfaceConstraint.createForAssemblyContext Method

Parent Object: [PerpendicularToSurfaceConstraint](PerpendicularToSurfaceConstraint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"perpendicularToSurfaceConstraint_var" is a variable referencing a [PerpendicularToSurfaceConstraint](PerpendicularToSurfaceConstraint.md) object.

```python
returnValue = perpendicularToSurfaceConstraint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [PerpendicularToSurfaceConstraint](PerpendicularToSurfaceConstraint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2023  

