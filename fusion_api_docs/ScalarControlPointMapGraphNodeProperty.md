
Derived from: [GraphNodeProperty](GraphNodeProperty.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

A property value that defines a complex mapping curve from an input domain of double values to an output range of double values. The mapping is represented by a set of points ordered by their domain value parameters. For a given input value, the output value is interpolated from the values of the two points before and after it using the specified interpolation function for each point.

## Methods

| Name | Description |
|----|----|
| [addPoint](ScalarControlPointMapGraphNodeProperty_addPoint.md) | Add a point to the map. |
| [classType](ScalarControlPointMapGraphNodeProperty_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](ScalarControlPointMapGraphNodeProperty_clear.md) | Remove all points from the map. |
| [getPoint](ScalarControlPointMapGraphNodeProperty_getPoint.md) | Get the point at index. |
| [removePoint](ScalarControlPointMapGraphNodeProperty_removePoint.md) | Remove a point from the map. |

## Properties

| Name | Description |
| --- | --- |
| [description](ScalarControlPointMapGraphNodeProperty_description.md) | Returns the description of this property. This description is localized and can change based on the current language. |
| [isValid](ScalarControlPointMapGraphNodeProperty_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ScalarControlPointMapGraphNodeProperty_name.md) | Gets the internal name of the property. |
| [objectType](ScalarControlPointMapGraphNodeProperty_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [pointCount](ScalarControlPointMapGraphNodeProperty_pointCount.md) | The number of points. |

## Version

Introduced in version May 2025  

