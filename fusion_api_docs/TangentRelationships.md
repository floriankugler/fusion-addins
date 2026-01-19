# TangentRelationships Object

Derived from: [Base](Base.md) Object  

## Description

The collection of Tangent Relationships in this component. This provides access to all existing tangent relationships and supports the ability to create new tangent relationships.

## Methods

| Name | Description |
|----|----|
| [add](TangentRelationships_add.md) | Creates a new tangent relationship between two components. |
| [classType](TangentRelationships_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](TangentRelationships_createInput.md) | Creates a TangentRelationshipInput object, which is the API equivalent to the Tangent Relationship command dialog. You use methods and properties on the returned class to set the desired options, similar to providing input in the Tangent Relationship command dialog. Once the settings are defined you call the TangentRelationships.add method passing in the TangentRelationshipInput object to create the actual TangentRelationship. |
| [item](TangentRelationships_item.md) | Function that returns the specified tangent relationship using an index into the collection. |
| [itemByName](TangentRelationships_itemByName.md) | Function that returns the specified tangent relationship using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](TangentRelationships_count.md) | Returns number of TangentRelationship objects in the collection. |
| [isValid](TangentRelationships_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TangentRelationships_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.tangentRelationships](Component_tangentRelationships.md), [FlatPatternComponent.tangentRelationships](FlatPatternComponent_tangentRelationships.md)

## Version

Introduced in version May 2022  

