# RemoveFeature.itemToRemove Property

Parent Object: [RemoveFeature](RemoveFeature.md)  

## Description

Gets and sets the body or component occurrence to remove.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"removeFeature_var" is a variable referencing a RemoveFeature object.  

```python
# Get the value of the property.
propertyValue = removeFeature_var.itemToRemove
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version September 2015  

