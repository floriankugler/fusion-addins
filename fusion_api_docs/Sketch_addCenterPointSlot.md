# Sketch.addCenterPointSlot Method

Parent Object: [Sketch](Sketch.md)  

## Description

Creates the geometry that represents a slot where the first point defines the center of the slot and the second point defines the direction and half-length. Geometric constraints are automatically added to the geometry to maintain the slot shape and optionally, dimensions to control the size can be added. The created geometry and constraints are returned.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
# Uses no optional arguments.
returnValue = sketch_var.addCenterPointSlot(centerPoint, endPoint, width)

# Uses optional arguments.
returnValue = sketch_var.addCenterPointSlot(centerPoint, endPoint, width, createWidthDimension, halfLength, angle)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md)\[\] | Returns an array containing the start point arc, the end point arc, the two lines that define the slot, the construction line between the start and end point, and optionally, the construction line the angle is measured from if an angle is specified, and the dimension constraints that were created in the order of width, half length, and angle. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| centerPoint | [Base](Base.md) | The center point of the slot. It can be a SketchPoint or Point3D object. If a SketchPoint is provided a coincident constraint will be created between the center point of the slot and the provided sketch point. |
| endPoint | [Base](Base.md) | A point that defines the direction and half-length of the slot. It can be a SketchPoint or Point3D object. The distance from the center point to this point represents half the total length of the slot. If a SketchPoint is provided a coincident constraint is created between the end point of the slot and the provided sketch point. If the halfLength or angle arguments are provided, the point is not the actual end point but is used to determine the direction of the slot. If both the halfLength and angle arguments are provided this endPoint will be ignored and null can be provided. |
| width | [ValueInput](ValueInput.md) | A ValueInput object that defines the width of the slot. The ValueInput can define either a real value or an expression string. If it is a real value, it defines the width of the slot in centimeters. When using a ValueInput created using a string, it's the same as creating a parameter in the user-interface. You can specify any valid expression, i.e. "5", "5 in", "5 in / 2", "5 + Length" that defines a length. |
| createWidthDimension | boolean | Specifies if a dimension constraint and its associated parameter is created to control the width of the slot. This is an optional argument whose default value is False. |
| halfLength | [ValueInput](ValueInput.md) | Optional argument that defines half the length of the slot using a ValueInput. If this is provided, it overrides the endPoint distance and explicitly defines half the length of the slot. If the half length is specified, a dimension constraint and its associated parameter is created to control the length. The ValueInput can define either a real value or an expression string. If it is a real value, it defines half the length of the slot in centimeters. When it is an expression string, it's the same as creating a parameter in the user-interface. You can specify any valid expression, i.e. "2.5", "2.5 in", "5 in / 4", "HalfLength" that defines a length. This is an optional argument whose default value is null. |
| angle | [ValueInput](ValueInput.md) | Optional argument that defines the angle of the slot using a ValueInput. If this is provided, it overrides the endPoint and explicitly defines the angle of the slot. If the angle is specified, a horizontal construction line, a dimension constraint, and its associated parameter is created to control the angle. The angle is measured from a horizontal line that starts at the center point and goes in the positive X direction. The angle is always less than 180 deg. and depending on the location of the direction point, the angle will be clockwise or counterclockwise from the horizontal line. The ValueInput can define either a real value or an expression string. If it is a real value, it defines the angle of the slot in radians. When it is an expression string, it's the same as creating a parameter in the user-interface. You can specify any valid expression, i.e. "45", "45 deg", "180 / 3", "Sweep * 2" that defines an angle. This is an optional argument whose default value is null. |

## Version

Introduced in version November 2025  

