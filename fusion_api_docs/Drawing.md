# Drawing Object

Derived from: [Product](Product.md) Object  

## Description

Object that represents the drawing specific data within a drawing document.

## Methods

| Name | Description |
| --- | --- |
| [classType](Drawing_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteEntities](Drawing_deleteEntities.md) | Deletes the specified set of entities that are associated with this product. |
| [findAttributes](Drawing_findAttributes.md) | Find attributes attached to objects in this product that match the group and or attribute name. This does not find attributes attached directly to the Product or Document objects but finds the attributes attached to entities within the product. The search string for both the groupName and attributeName arguments can be either an absolute name value, or a regular expression. With an absolute name, the search string must match the entire groupName or attributeName, including case. An empty string will match everything. For example if you have an attribute group named "MyStuff" that contains the attribute "Length1", using the search string "MyStuff" as the group name and "Length1" as the attribute name will find the attributes with those names. Searching for "MyStuff" as the group name and "" as the attribute name will find all attributes that have "MyStuff" as the group name. Regular expressions provide a more flexible way of searching. To use a regular expression, prefix the input string for the groupName or attributeName arguments with "re:". The regular expression much match the entire group or attribute name. For example if you have a group that contains attributes named "Length1", "Length2", "Width1", and "Width2" and want to find any of the length attributes you can use a regular expression using the string "re:Length.*". For more information on attributes see the Attributes topic in the user manual. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](Drawing_attributes.md) | Returns the collection of attributes associated with this product. |
| [exportManager](Drawing_exportManager.md) | Returns the DrawingExportManager for this drawing. You use the ExportManager to export the drawing in various formats. |
| [isValid](Drawing_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [namedViews](Drawing_namedViews.md) | Returns the NamedViews object associated with this product. The NamedViews collection provides access to the named views defined in this product and supports the creation of new named views. |
| [objectType](Drawing_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentDocument](Drawing_parentDocument.md) | Returns the parent Document object. |
| [productType](Drawing_productType.md) | Returns the product type name of this product. A list of all of the possible product types can be obtained by using the Application.supportedProductTypes property. |
| [selectionSets](Drawing_selectionSets.md) | Returns the SelectionSets object associated with this product. If the product does not support selection sets, null is returned. The SelectionSets object is used to create and access existing selection sets. |
| [unitsManager](Drawing_unitsManager.md) | Returns the UnitsManager object associated with this product. |
| [workspaces](Drawing_workspaces.md) | Returns the workspaces associated with this product. |

## Accessed From

[DrawingDocument.drawing](DrawingDocument_drawing.md)

## Version

Introduced in version December 2020  

