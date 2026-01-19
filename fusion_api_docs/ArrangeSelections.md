# ArrangeSelections Object

Derived from: [Base](Base.md) Object  

## Description

Collection for all arrange selections to be passed to a CAMArrangeParameterValue object. This is a read-only container. It returns the arrange selections associated with the parent parameter value object, but does not write to it. To apply changes done to the collection and the selections it contains, CAMArrangeParameterValue.applyArrangeSelections() needs to be called.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeSelections_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](ArrangeSelections_clear.md) | Clears all entries. |
| [createNewArrangeSelection](ArrangeSelections_createNewArrangeSelection.md) | Creates a new occurrence selection meant for arrange operations and adds it to the end of the collection. |
| [item](ArrangeSelections_item.md) | Function that returns the specified arrange selection object using an index into the collection. |
| [remove](ArrangeSelections_remove.md) | Function that removes the specified arrange selection object using an index in the collection. |
| [removeByObject](ArrangeSelections_removeByObject.md) | Function that removes the specified arrange selection object from the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](ArrangeSelections_count.md) | The number of items in the collection. |
| [isValid](ArrangeSelections_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeSelections_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMArrangeParameterValue.getArrangeSelections](CAMArrangeParameterValue_getArrangeSelections.md)

## Version

Introduced in version March 2024  

