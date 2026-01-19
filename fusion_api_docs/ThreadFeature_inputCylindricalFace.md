# ThreadFeature.inputCylindricalFace Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets and sets the threaded face. In the case where there are multiple faces, only the first one is returned. Setting this results in a thread being applied to only a single face. It is recommended that you use the inputCylindricalfaces property in order to have full access to the collection of faces to be threaded.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

If the thread feature is associated with a hole (the hole property is not null), this property will always return null and will fail if set.

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.inputCylindricalFace

# Set the value of the property.
threadFeature_var.inputCylindricalFace = propertyValue
```

## Property Value

This is a read/write property whose value is a [BRepFace](BRepFace.md).

## Version

Introduced in version November 2015  

