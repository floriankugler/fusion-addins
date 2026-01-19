# PlanarJointMotion.customPrimarySlideDirectionEntity Property

Parent Object: [PlanarJointMotion](PlanarJointMotion.md)  

## Description

This property can be set using various types of entities that can infer a direction. For example, a linear edge, sketch line, planar face, and cylindrical face. When reading this property, it is only valid in the case where the primarySlideDirection property returns CustomJointDirection. Setting this property will automatically set the primarySlideDirection property to CustomJointDirection. The entity defining the custom direction by be perpendicular to the normal direction.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"planarJointMotion_var" is a variable referencing a PlanarJointMotion object.  

```python
# Get the value of the property.
propertyValue = planarJointMotion_var.customPrimarySlideDirectionEntity

# Set the value of the property.
planarJointMotion_var.customPrimarySlideDirectionEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

