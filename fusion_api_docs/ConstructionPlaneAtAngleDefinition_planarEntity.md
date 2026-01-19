# ConstructionPlaneAtAngleDefinition.planarEntity Property

Parent Object: [ConstructionPlaneAtAngleDefinition](ConstructionPlaneAtAngleDefinition.md)  

## Description

Gets the planar face or construction plane the angle for this construction plane is measured from and is parametrically dependent on.  

This property is only valid for construction planes that were created using the API. When an angle construction plane is created using the user interface the plane is not defined by the user and a plane is automatically inferred by Fusion. In this case, this property will return null.

## Syntax

"constructionPlaneAtAngleDefinition_var" is a variable referencing a ConstructionPlaneAtAngleDefinition object.  

```python
# Get the value of the property.
propertyValue = constructionPlaneAtAngleDefinition_var.planarEntity
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

