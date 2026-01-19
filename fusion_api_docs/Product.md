# Product Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the various product specific containers. For Fusion this is the Design object. For manufacturing this is a CAM object.

## Methods

| Name | Description |
| --- | --- |
| [classType](Product_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteEntities](Product_deleteEntities.md) | Deletes the specified set of entities that are associated with this product. |
| [findAttributes](Product_findAttributes.md) | Find attributes attached to objects in this product that match the group and or attribute name. This does not find attributes attached directly to the Product or Document objects but finds the attributes attached to entities within the product. The search string for both the groupName and attributeName arguments can be either an absolute name value, or a regular expression. With an absolute name, the search string must match the entire groupName or attributeName, including case. An empty string will match everything. For example if you have an attribute group named "MyStuff" that contains the attribute "Length1", using the search string "MyStuff" as the group name and "Length1" as the attribute name will find the attributes with those names. Searching for "MyStuff" as the group name and "" as the attribute name will find all attributes that have "MyStuff" as the group name. Regular expressions provide a more flexible way of searching. To use a regular expression, prefix the input string for the groupName or attributeName arguments with "re:". The regular expression much match the entire group or attribute name. For example if you have a group that contains attributes named "Length1", "Length2", "Width1", and "Width2" and want to find any of the length attributes you can use a regular expression using the string "re:Length.*". For more information on attributes see the Attributes topic in the user manual. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](Product_attributes.md) | Returns the collection of attributes associated with this product. |
| [isValid](Product_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [namedViews](Product_namedViews.md) | Returns the NamedViews object associated with this product. The NamedViews collection provides access to the named views defined in this product and supports the creation of new named views. |
| [objectType](Product_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentDocument](Product_parentDocument.md) | Returns the parent Document object. |
| [productType](Product_productType.md) | Returns the product type name of this product. A list of all of the possible product types can be obtained by using the Application.supportedProductTypes property. |
| [selectionSets](Product_selectionSets.md) | Returns the SelectionSets object associated with this product. If the product does not support selection sets, null is returned. The SelectionSets object is used to create and access existing selection sets. |
| [unitsManager](Product_unitsManager.md) | Returns the UnitsManager object associated with this product. |
| [workspaces](Product_workspaces.md) | Returns the workspaces associated with this product. |

## Accessed From

[Application.activeProduct](Application_activeProduct.md), [FusionUnitsManager.product](FusionUnitsManager_product.md), [NamedView.parentProduct](NamedView_parentProduct.md), [Products.item](Products_item.md), [Products.itemByProductType](Products_itemByProductType.md), [RenderManager.parentDesign](RenderManager_parentDesign.md), [UnitsManager.product](UnitsManager_product.md)

## Derived Classes

[CAM](CAM.md), [Design](Design.md), [Drawing](Drawing.md)

## Samples

| Name | Description |
|----|----|
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

