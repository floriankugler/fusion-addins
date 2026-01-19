# VariableRadiusFilletEdgeSetInput Object

Derived from: [FilletEdgeSetInput](FilletEdgeSetInput.md) Object  

## Description

Provides access to the edges and the parameters associated with a variable radius fillet.

## Methods

| Name | Description |
|----|----|
| [classType](VariableRadiusFilletEdgeSetInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setMidRadii](VariableRadiusFilletEdgeSetInput_setMidRadii.md) | Defines any additional points along the fillet where a radius is specified. |

## Properties

| Name | Description |
| --- | --- |
| [continuity](VariableRadiusFilletEdgeSetInput_continuity.md) | Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. The default is TangentSurfaceContinuityType. For an asymmetric fillet edge set, this must always be tangent continuity (G1) and setting it to another value will fail. |
| [endRadius](VariableRadiusFilletEdgeSetInput_endRadius.md) | Gets and sets a ValueInput object that defines the ending radius of the fillet. If a single edge is being filleted, the end radius is at the end of the edge. If multiple tangent edges are being filleted the end radius is the open end of the last edge in the collection. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| [entities](VariableRadiusFilletEdgeSetInput_entities.md) | Gets and sets the entities associated with this fillet edge set. For constant radius and chord length edge sets, this can be edges, faces, and features. For variable radius edges sets, this must be edges. |
| [isValid](VariableRadiusFilletEdgeSetInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](VariableRadiusFilletEdgeSetInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [startRadius](VariableRadiusFilletEdgeSetInput_startRadius.md) | Gets and sets a ValueInput object that defines the starting radius of the fillet. If a single edge is being filleted, the start radius is at the start end of the edge. If multiple tangent edges are being filleted the start radius is the start end of the first edge in the collection. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| [tangencyWeight](VariableRadiusFilletEdgeSetInput_tangencyWeight.md) | Gets and sets the tangency weight for the given edge set. The tangency weight controls the influence of the continuity (G1 or G2) on the fillet. The ValueInput must be a real value between 0.1 and 2.0 inclusive, with no units. The default value is 1.0. |

## Accessed From

[FilletEdgeSetInputs.addVariableRadiusEdgeSet](FilletEdgeSetInputs_addVariableRadiusEdgeSet.md)

## Version

Introduced in version November 2022  

