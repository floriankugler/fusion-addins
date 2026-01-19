# NamedView Object

Derived from: [Base](Base.md) Object  

## Description

Represents a named view as seen in the browser.

## Methods

| Name | Description |
|----|----|
| [apply](NamedView_apply.md) | This updates the active viewport to use the camera associated with this named view. |
| [classType](NamedView_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](NamedView_deleteMe.md) | Deletes this named view. This method will fail for any of the four standard named views. This can be determined by checking to see if the isBuiltIn property is true. |

## Properties

| Name | Description |
| --- | --- |
| [camera](NamedView_camera.md) | Gets and sets the camera associated with this named view. This property acts as read-only for the four standard named views. This can be determined by checking to see if the isBuiltIn property is true. |
| [isBuiltIn](NamedView_isBuiltIn.md) | Indicates if this named view is one of the four standard named views ("TOP", "FRONT", "RIGHT", and "HOME"). There is limited functionality with the four standard named views. |
| [isValid](NamedView_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](NamedView_name.md) | Gets and sets the name of this named view. This property acts as read-only for the four standard named views. This can be determined by checking to see if the isBuiltIn property is true. |
| [objectType](NamedView_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentProduct](NamedView_parentProduct.md) | Returns the parent product of this named view. |

## Accessed From

[NamedViews.add](NamedViews_add.md), [NamedViews.frontNamedView](NamedViews_frontNamedView.md), [NamedViews.homeNamedView](NamedViews_homeNamedView.md), [NamedViews.item](NamedViews_item.md), [NamedViews.itemByName](NamedViews_itemByName.md), [NamedViews.rightNamedView](NamedViews_rightNamedView.md), [NamedViews.topNamedView](NamedViews_topNamedView.md)

## Version

Introduced in version September 2023  

