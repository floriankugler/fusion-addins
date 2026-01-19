# ConstructionAxes Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the construction axes within a component and provides methods to create new construction axes.

## Methods

| Name | Description |
| --- | --- |
| [add](ConstructionAxes_add.md) | Creates and adds a new ConstructionAxis using the creation parameters in the ConstructionAxisInput. If the ConstructionAxisInput was defined using the setByLine method then the add will only work in the direct modeling mode and will fail in the parametric modeling mode. |
| [classType](ConstructionAxes_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ConstructionAxes_createInput.md) | Create a ConstructionAxisInput object that is in turn used to create a ConstructionAxis. |
| [item](ConstructionAxes_item.md) | Function that returns the specified construction axis using an index into the collection. |
| [itemByName](ConstructionAxes_itemByName.md) | Returns the specified construction axis using the name of the construction axis as it is displayed in the browser. |

## Properties

| Name | Description |
| --- | --- |
| [component](ConstructionAxes_component.md) | The component that owns this collection. |
| [count](ConstructionAxes_count.md) | The number of construction axes in the collection. |
| [isValid](ConstructionAxes_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionAxes_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BaseComponent.constructionAxes](BaseComponent_constructionAxes.md), [Component.constructionAxes](Component_constructionAxes.md), [FlatPatternComponent.constructionAxes](FlatPatternComponent_constructionAxes.md)

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

