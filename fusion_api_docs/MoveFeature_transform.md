# MoveFeature.transform Property

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the move transform of the input bodies or faces.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Remarks

This property is obsolete. The move feature now supports more than a simple transform. This property can still work in the case where a move feature was created using the FreeMove type of move but will fail in all other cases.

## Syntax

"moveFeature_var" is a variable referencing a MoveFeature object.  

```python
# Get the value of the property.
propertyValue = moveFeature_var.transform

# Set the value of the property.
moveFeature_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version March 2015  
Retired in version January 2023  

