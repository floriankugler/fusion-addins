# ToEntityExtentDefinition.create Method

Parent Object: [ToEntityExtentDefinition](ToEntityExtentDefinition.md)  

## Description

Statically creates a new ToEntityExtentDefinition object. This is used as input when defining the extents of a feature to be up to a construction plane or face.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.fusion.ToEntityExtentDefinition.create(entity, isChained)

# Uses optional arguments.
returnValue = adsk.fusion.ToEntityExtentDefinition.create(entity, isChained, offset)
```

## Return Value

| Type | Description |
|----|----|
| [ToEntityExtentDefinition](ToEntityExtentDefinition.md) | Returns the newly created ToEntityExtentDefinition object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entity | [Base](Base.md) | The construction plane or face that the feature extent it up to. |
| isChained | boolean |  |
| offset | [ValueInput](ValueInput.md) | A optional input value that defines an offset distance of the entity that will be used for the extent. Positive and negative values can be used to offset in both directions. If this argument is not provided a value of zero will be used. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [extrudeFeatures.add using setTwoSidesExtent](extrudeFeaturesTwoSidesExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setTwoSidesExtent method. To use this sample have a design open that contains a profile and a body that is positioned away from the profile but is a size where when the profile is extruded it will intersect the body. When you run the script you will be prompted to select the profile that will be used to create the extrusion and the body to extrude to. The extrusion will be created up to the body with an offset and will also be offset from the sketch plane. |

## Version

Introduced in version November 2016  

