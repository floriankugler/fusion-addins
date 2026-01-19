# SliderJointMotion.customSlideDirectionEntity Property

Parent Object: [SliderJointMotion](SliderJointMotion.md)  

## Description

This property can be set using various types of entities that can infer a direction. For example, a linear edge, sketch line, planar face, and cylindrical face. This property is only valid in the case where the slideDirection property returns CustomJointDirection. Setting this property will automatically set the slideDirection property to CustomJointDirection.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"sliderJointMotion_var" is a variable referencing a SliderJointMotion object.  

```python
# Get the value of the property.
propertyValue = sliderJointMotion_var.customSlideDirectionEntity

# Set the value of the property.
sliderJointMotion_var.customSlideDirectionEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

