# ConstructionPoints Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the construction points within a component and provides methods to create new construction points.

## Methods

| Name | Description |
| --- | --- |
| [add](ConstructionPoints_add.md) | Creates a new construction point. If the ConstructionPointInput was defined using the setByPoint method using a Point3D object then the add will only work in the direct modeling mode and will fail in the parametric modeling mode. |
| [classType](ConstructionPoints_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ConstructionPoints_createInput.md) | Create a ConstructionPointInput object that is in turn used to create a ConstructionPoint. |
| [item](ConstructionPoints_item.md) | Function that returns the specified construction point using an index into the collection. |
| [itemByName](ConstructionPoints_itemByName.md) | Returns the specified construction point using the name of the construction point as it is displayed in the browser. |

## Properties

| Name | Description |
| --- | --- |
| [component](ConstructionPoints_component.md) | The component that owns this collection. |
| [count](ConstructionPoints_count.md) | The number of construction points in the collection. |
| [isValid](ConstructionPoints_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPoints_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BaseComponent.constructionPoints](BaseComponent_constructionPoints.md), [Component.constructionPoints](Component_constructionPoints.md), [FlatPatternComponent.constructionPoints](FlatPatternComponent_constructionPoints.md)

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

