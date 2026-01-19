# MeshRemeshFeatures.classType Method

Parent Object: [MeshRemeshFeatures](MeshRemeshFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType().

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.MeshRemeshFeatures.classType()
```

## Return Value

| Type   | Description                                         |
|--------|-----------------------------------------------------|
| string | Returns a string indicating the type of the object. |

## Version

Introduced in version March 2024  

