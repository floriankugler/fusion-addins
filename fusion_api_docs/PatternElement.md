# PatternElement Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the properties that pertain to the pattern element.

## Methods

| Name | Description |
|----|----|
| [classType](PatternElement_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [faces](PatternElement_faces.md) | Gets the faces generated as a result of this particular element. |
| [id](PatternElement_id.md) | Gets the id of this element within the pattern. |
| [isSuppressed](PatternElement_isSuppressed.md) | Gets and sets whether the element is suppressed or not. A value of True indicates it is suppressed |
| [isValid](PatternElement_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](PatternElement_name.md) | Get the name of the pattern element. |
| [objectType](PatternElement_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrences](PatternElement_occurrences.md) | If the patternEntityType property of the parent feature returns OccurrencesPatternType then this property will return the occurrences associated with this particular pattern element. |
| [parentFeature](PatternElement_parentFeature.md) | Gets the feature pattern this element is a member of. |
| [transform](PatternElement_transform.md) | Get the transform that describes this elements relative position to the parent object(s). The transform returned for the first element in a pattern will be an identity matrix. |

## Accessed From

[PatternElements.item](PatternElements_item.md)

## Version

Introduced in version November 2014  

