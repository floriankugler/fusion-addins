# RuledSurfaceFeatures.createInput Method

Parent Object: [RuledSurfaceFeatures](RuledSurfaceFeatures.md)  

## Description

Creates a RuledSurfaceFeatureInput object that defines the input needed to create a ruled surface feature. Use the input object to define the input to create the desired feature and then use the Add method, passing in the RuledSurfaceFeatureInput object.

## Syntax

"ruledSurfaceFeatures_var" is a variable referencing a [RuledSurfaceFeatures](RuledSurfaceFeatures.md) object.

```python
# Uses no optional arguments.
returnValue = ruledSurfaceFeatures_var.createInput(profile, distance, angle, ruledSurfaceType)

# Uses optional arguments.
returnValue = ruledSurfaceFeatures_var.createInput(profile, distance, angle, ruledSurfaceType, direction)
```

## Return Value

| Type | Description |
|----|----|
| [RuledSurfaceFeatureInput](RuledSurfaceFeatureInput.md) | Returns the newly created RuledSurfaceFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| profile | [Base](Base.md) | A Profile object that defines the sketch geometry or edges that define the shape of the ruled surface. The Component.createBRepEdgeProfile method is useful to create a profile defined from edges. |
| distance | [ValueInput](ValueInput.md) | ValueInput object that defines the extension distance of the Ruled Surface.. |
| angle | [ValueInput](ValueInput.md) | ValueInput object that defines angle to use when creating the Ruled Surface. When the input is a real value, the units are radians. |
| ruledSurfaceType | [RuledSurfaceTypes](RuledSurfaceTypes.md) | The Ruled Surface type (TangentRuledSurfaceType, NormalRuledSurfaceType, or DirectionRuledSurfaceType). |
| direction | [Base](Base.md) | If the ruled surface type is DirectionRuledSurfaceType, you must specify the direction. The direction is specified by providing a linear or planar entity. For example, a linear edge, construction axis, planar face, or construction plane can be used as input. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2020  

