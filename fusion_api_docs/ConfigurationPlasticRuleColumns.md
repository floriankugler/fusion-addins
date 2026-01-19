# ConfigurationPlasticRuleColumns Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the columns in a plastic rule table. This collection can be empty when no columns have been created. When the table is empty, it is not displayed in the user interface, and adding a column causes the table to be displayed.

## Methods

| Name | Description |
|----|----|
| [add](ConfigurationPlasticRuleColumns_add.md) | Adds a new column to the plastic rule table. |
| [classType](ConfigurationPlasticRuleColumns_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ConfigurationPlasticRuleColumns_item.md) | A method that returns the specified column using an index into the collection. These are returned in the same order as they appear in the table. |
| [itemById](ConfigurationPlasticRuleColumns_itemById.md) | A method that returns the column with the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](ConfigurationPlasticRuleColumns_count.md) | Returns the number of columns in the table where the name column is not included. |
| [isValid](ConfigurationPlasticRuleColumns_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationPlasticRuleColumns_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ConfigurationPlasticRuleTable.columns](ConfigurationPlasticRuleTable_columns.md)

## Version

Introduced in version January 2024  

