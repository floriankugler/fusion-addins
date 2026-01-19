# ThreadFeature.inputCylindricalFaces Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets and sets the cylindrical input faces.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

If the thread feature is associated with a hole (the hole property is not null), this property will always return null and will fail if set.

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.inputCylindricalFaces

# Set the value of the property.
threadFeature_var.inputCylindricalFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2015  

