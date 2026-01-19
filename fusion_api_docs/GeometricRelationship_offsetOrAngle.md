# GeometricRelationship.offsetOrAngle Property

Parent Object: [GeometricRelationship](GeometricRelationship.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This property is used when the geometric relationship is associated with an existing joint or assembly constraint (the isTemporary property is false). It returns the parameter that controls the offset or angle of this geometric relationship. You can change the value by editing properties on the returned ModelParameter object.  

If this geometric relationship is associated with a JointInput object (the isTemporary property is true), this property returns null, and you should use the offsetOrAngleValue property to get and set the value.

## Syntax

"geometricRelationship_var" is a variable referencing a GeometricRelationship object.  

```python
# Get the value of the property.
propertyValue = geometricRelationship_var.offsetOrAngle
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version July 2025  

