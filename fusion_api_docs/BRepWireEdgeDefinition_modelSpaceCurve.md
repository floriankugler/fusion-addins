# BRepWireEdgeDefinition.modelSpaceCurve Property

Parent Object: [BRepWireEdgeDefinition](BRepWireEdgeDefinition.md)  

## Description

Gets and sets the Curve3D object that defines the shape of the edge using 3D geometry in model space. Valid objects are an Arc3D, NurbsCurve3D, Circle3D, Ellipse3D, EllipticalArc3D, or Line3D.

## Syntax

"bRepWireEdgeDefinition_var" is a variable referencing a BRepWireEdgeDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepWireEdgeDefinition_var.modelSpaceCurve

# Set the value of the property.
bRepWireEdgeDefinition_var.modelSpaceCurve = propertyValue
```

## Property Value

This is a read/write property whose value is a [Curve3D](Curve3D.md).

## Version

Introduced in version September 2020  

