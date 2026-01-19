# SweepFeature.solidBody Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the BRepBody object to sweep. It must be a solid body. Setting this property results in the type being a single path sweep, and if the profile, guide path, or surface are set, they are set to null.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.solidBody

# Set the value of the property.
sweepFeature_var.solidBody = propertyValue
```

## Property Value

This is a read/write property whose value is a [BRepBody](BRepBody.md).

## Version

Introduced in version May 2024  

