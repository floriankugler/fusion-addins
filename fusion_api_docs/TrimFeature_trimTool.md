# TrimFeature.trimTool Property

Parent Object: [TrimFeature](TrimFeature.md)  

## Description

Gets and sets the entity (a patch body, B-Rep face, construction plane or sketch curve) that intersects the trim tool.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"trimFeature_var" is a variable referencing a TrimFeature object.  

```python
# Get the value of the property.
propertyValue = trimFeature_var.trimTool

# Set the value of the property.
trimFeature_var.trimTool = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

