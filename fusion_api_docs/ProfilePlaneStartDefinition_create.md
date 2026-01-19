# ProfilePlaneStartDefinition.create Method

Parent Object: [ProfilePlaneStartDefinition](ProfilePlaneStartDefinition.md)  

## Description

Statically creates a new ProfilePlaneStartDefinition object. This is used as input when creating a new feature and defining the starting condition.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.ProfilePlaneStartDefinition.create()
```

## Return Value

| Type | Description |
|----|----|
| [ProfilePlaneStartDefinition](ProfilePlaneStartDefinition.md) | Returns the newly created ProfilePlaneStartDefinition object or null in the case of a failure. |

## Samples

| Name | Description |
|----|----|
| [extrudeFeatures.add using thin extrude](extrudeFeaturesThin_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setThinExtrude method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the thin extrusion. |

## Version

Introduced in version November 2016  

