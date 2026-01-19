# AsBuiltJoint.geometry Property

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Specifies the position of the joint. Getting this property will return null and setting it will be ignored in the case where the joint motion is rigid.  

To set this property, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True)

## Syntax

"asBuiltJoint_var" is a variable referencing an AsBuiltJoint object.  

```python
# Get the value of the property.
propertyValue = asBuiltJoint_var.geometry

# Set the value of the property.
asBuiltJoint_var.geometry = propertyValue
```

## Property Value

This is a read/write property whose value is a [JointGeometry](JointGeometry.md).

## Version

Introduced in version September 2015  

