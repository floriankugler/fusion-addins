# GeometricRelationship.redefineOffsetOrAngle Method

Parent Object: [GeometricRelationship](GeometricRelationship.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This method redefines an existing geometric relationship by defining if it is a mate or angle and specifying a new value.  

If the GeometricRelationship is associated with an existing joint or assembly constraint (the isTemporary property is false), you need to position the timeline marker immediately before the joint or assembly constraint. This can be accomplished using the following code: thisJointOrConstraint.timelineObject.rollTo(True).

## Syntax

"geometricRelationship_var" is a variable referencing a [GeometricRelationship](GeometricRelationship.md) object.

```python
returnValue = geometricRelationship_var.redefineOffsetOrAngle(isMate, offsetOrAngleValue)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if the redefinition was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isMate | boolean | This argument indicates if the geometric relationship defines a mate or an angle. A value of true indicates a mate relationship. |
| offsetOrAngleValue | [ValueInput](ValueInput.md) | This argument specifies the value associated with the geometric relationship. If isMate is true, the value is a length, and if it is a real value, then it is centimeters. If it is a string, it is an expression that must evaluate to a length. If isMate is False, the value is an angle, and if it is a real value, then it is radians. If it is a string, it is an expression that must evaluate to an angle. |

## Version

Introduced in version July 2025  

