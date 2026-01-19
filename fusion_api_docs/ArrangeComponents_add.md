# ArrangeComponents.add Method

Parent Object: [ArrangeComponents](ArrangeComponents.md)  

## Description

Adds a new ArrangeComponent object to the collection.

## Syntax

"arrangeComponents_var" is a variable referencing an [ArrangeComponents](ArrangeComponents.md) object.

```python
returnValue = arrangeComponents_var.add(occurrenceOrFace)
```

## Return Value

| Type | Description |
|----|----|
| [ArrangeComponent](ArrangeComponent.md) | Returns the created ArrangeComponent where you can use properties on it to define the various other settings supported to control how the component is arranged. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| occurrenceOrFace | [Base](Base.md) | For a 2D arrange this can be an Occurrence or BRepFace object that defines which component to use. If a BRepFace object is used, the face is used to orient the part in the arrangement and will face up or down depending on the isGlobalDirectionFaceUp property on the ArrangeFeature2DInput object. For a 2D arrange, if an Occurrence is provided, the Occurrence will be oriented in the arrangement such that the largest face points downward. For a 3D arrange this can be an Occurrence or BRepFace object but if a BRepFace is provided it does not define the orientation but is only used to get the parent Occurrence. For a 3D arrange the arranged occurrences have the same orientation as the original occurrence but are positioned within the 3D envelope. |

## Version

Introduced in version January 2025  

