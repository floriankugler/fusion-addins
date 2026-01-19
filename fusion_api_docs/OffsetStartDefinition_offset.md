# OffsetStartDefinition.offset Property

Parent Object: [OffsetStartDefinition](OffsetStartDefinition.md)  

## Description

Gets the currently defined offset value. If the ProfilePlaneWithOffsetDefinition object was created statically and is not associated with a feature, this will return a ValueInput object. if the ProfilePlaneWithOffsetDefinition is associated with an existing feature, this will return the parameter that was created when the feature was created. To edit the offset, use properties on the parameter to change the value of the parameter.

## Syntax

"offsetStartDefinition_var" is a variable referencing an OffsetStartDefinition object.  

```python
# Get the value of the property.
propertyValue = offsetStartDefinition_var.offset
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

