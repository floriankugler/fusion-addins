# RevolveFeature.participantBodies Property

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"revolveFeature_var" is a variable referencing a RevolveFeature object.  

```python
# Get the value of the property.
propertyValue = revolveFeature_var.participantBodies

# Set the value of the property.
revolveFeature_var.participantBodies = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepBody](BRepBody.md).

## Version

Introduced in version January 2017  

