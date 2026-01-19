# ArrangeComponent.setRotationUsingEdge Method

Parent Object: [ArrangeComponent](ArrangeComponent.md)  

## Description

Sets the rotation angle using the specified edge such that the edge is pointing in the zero rotation angle. This is a convenience method to set the rotation angle. The rotation property can be used to accomplish the same result.  

This is only valid for 2D True Shape arrangements and will fail for 2D rectangular and 3D arrangements.

## Syntax

"arrangeComponent_var" is a variable referencing an [ArrangeComponent](ArrangeComponent.md) object.

```python
returnValue = arrangeComponent_var.setRotationUsingEdge(edge)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edge | [BRepEdge](BRepEdge.md) | The BRepEdge object being used to define rotation of the component. |

## Version

Introduced in version January 2025  

