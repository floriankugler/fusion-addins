# Component.createOpenProfile Method

Parent Object: [Component](Component.md)  

## Description

Creates an open profile based on the input curve(s).

## Syntax

"component_var" is a variable referencing a [Component](Component.md) object.

```python
# Uses no optional arguments.
returnValue = component_var.createOpenProfile(curves)

# Uses optional arguments.
returnValue = component_var.createOpenProfile(curves, chainCurves)
```

## Return Value

| Type | Description |
|----|----|
| [Profile](Profile.md) | Returns the new Profile object or null in the case of a failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| curves | [Base](Base.md) | A SketchCurve or an ObjectCollection containing multiple sketch entities. If a single sketch curve is input the chainCurves argument is checked to determine if connected curves (they do not need to be tangent) should be automatically found. If multiple curves are provided the chainCurves argument is always treated as false so you must provide all of the curves in the object collection that you want included in the profile. The provided curves must all connect together in a single path. The input curves do not need to be in the same sketch, but they do need to geometrically connect for a valid profile to be created. |
| chainCurves | boolean | If true, this finds any curves within the same sketch that connect to the single input curve and automatically includes them in the profile. If false, only the curves provided will be used to define the profile. This argument is ignored and treated as false if multiple curves are input. This is an optional argument whose default value is True. |

## Version

Introduced in version June 2015  

