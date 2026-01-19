# ExtendFeature.edges Property

Parent Object: [ExtendFeature](ExtendFeature.md)  

## Description

Gets the edges that were extended. In many cases the extend operation results in the edges being consumed so they're no longer available after the feature is created. in this case you need to reposition the timeline marker to just before this feature when the edges do exist.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extendFeature_var" is a variable referencing an ExtendFeature object.  

```python
# Get the value of the property.
propertyValue = extendFeature_var.edges
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

