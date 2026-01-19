# SliderJointMotion.slideDirection Property

Parent Object: [SliderJointMotion](SliderJointMotion.md)  

## Description

Gets and sets the direction of the slide. This can be set to XAxisJointDirection, YAxisJointDirection, or ZAxisJointDirection. It can return those three directions and CustomJointDirection. If this returns CustomJointDirection then the customSlideDirectionEntity will return an entity that defines the direction. If there is a custom direction defined and this property is set to one of the three standard axes, the custom direction will be removed and customSlideDirectionEntity will return null.

## Syntax

"sliderJointMotion_var" is a variable referencing a SliderJointMotion object.  

```python
# Get the value of the property.
propertyValue = sliderJointMotion_var.slideDirection

# Set the value of the property.
sliderJointMotion_var.slideDirection = propertyValue
```

## Property Value

This is a read/write property whose value is a [JointDirections](JointDirections.md).

## Version

Introduced in version July 2015  

