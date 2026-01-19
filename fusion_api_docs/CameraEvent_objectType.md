# CameraEvent.objectType Property

Parent Object: [CameraEvent](CameraEvent.md)  

## Description

This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object.  

It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType():

## Syntax

"cameraEvent_var" is a variable referencing a CameraEvent object.  

```python
# Get the value of the property.
propertyValue = cameraEvent_var.objectType
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version December 2017  

