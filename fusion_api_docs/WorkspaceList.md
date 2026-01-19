# WorkspaceList Object

Derived from: [Base](Base.md) Object  

## Description

A WorkspaceList is a list of Workspaces - e.g. the Workspaces for a given product.

## Methods

| Name | Description |
|----|----|
| [classType](WorkspaceList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](WorkspaceList_item.md) | Returns the specified work space using an index into the collection. |
| [itemById](WorkspaceList_itemById.md) | Returns the Workspace of the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](WorkspaceList_count.md) | Gets the number of workspaces in the collection. |
| [isValid](WorkspaceList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](WorkspaceList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAM.workspaces](CAM_workspaces.md), [Design.workspaces](Design_workspaces.md), [Drawing.workspaces](Drawing_workspaces.md), [FlatPatternProduct.workspaces](FlatPatternProduct_workspaces.md), [Product.workspaces](Product_workspaces.md), [UserInterface.workspacesByProductType](UserInterface_workspacesByProductType.md), [WorkingModel.workspaces](WorkingModel_workspaces.md)

## Version

Introduced in version August 2014  

