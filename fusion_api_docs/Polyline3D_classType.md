# Polyline3D.classType Method

Parent Object: [Polyline3D](Polyline3D.md)  

## Description

Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType().

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Polyline3D.classType()
```

## Return Value

| Type   | Description                                         |
|--------|-----------------------------------------------------|
| string | Returns a string indicating the type of the object. |

## Version

Introduced in version September 2024  

