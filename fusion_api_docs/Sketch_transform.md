# Sketch.transform Property

Parent Object: [Sketch](Sketch.md)  

## Description

Gets and sets the transform of the sketch with respect to model space. This defines the transform from the parent component space to the sketch space. For example, if you have point coordinates in the space of the parent component and apply this transform it will result in the coordinates of the equivalent position in sketch space. The transform is sensitive to the assembly context.  

The position of a parametric sketch cannot be modified since its position is defined by its parametric association to other geometry. As a result this property will fail when called on a parametric sketch. Setting this property is only valid for sketches in a non-parametric design or sketches owned by a base feature.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.transform

# Set the value of the property.
sketch_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version August 2014  

