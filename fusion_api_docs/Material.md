# Material Object

Derived from: [Base](Base.md) Object  

## Description

A material.

## Methods

| Name | Description |
|----|----|
| [classType](Material_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copyTo](Material_copyTo.md) | \*\*RETIRED\*\* Copies this material to the specified target. |
| [deleteMe](Material_deleteMe.md) | Deletes the material from the Design. This method only applies to materials in a Design that are unused |

## Properties

| Name | Description |
| --- | --- |
| [appearance](Material_appearance.md) | Gets the Appearance of this material. |
| [description](Material_description.md) | Gets and sets the description associated with this material. Setting the description is only valid for materials in a document or the favorites list. |
| [id](Material_id.md) | Returns the unique internal ID of this material. |
| [isUsed](Material_isUsed.md) | Returns true if this material is used in the Design |
| [isValid](Material_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [materialProperties](Material_materialProperties.md) | Returns the collection of material properties associated with this material. |
| [name](Material_name.md) | Returns the name of this Material. This is the name of the material as seen in the user interface. The name can only be edited if the material is in a Design or the favorites list. |
| [objectType](Material_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](Material_parent.md) | Returns the Parent object (a Library or a Design). |

## Accessed From

[BRepBody.material](BRepBody_material.md), [Component.material](Component_material.md), [ConfigurationMaterialCell.material](ConfigurationMaterialCell_material.md), [FavoriteMaterials.add](FavoriteMaterials_add.md), [FavoriteMaterials.item](FavoriteMaterials_item.md), [FavoriteMaterials.itemById](FavoriteMaterials_itemById.md), [FavoriteMaterials.itemByName](FavoriteMaterials_itemByName.md), [FlatPatternComponent.material](FlatPatternComponent_material.md), [Material.copyTo](Material_copyTo.md), [MaterialPreferences.defaultMaterial](MaterialPreferences_defaultMaterial.md), [Materials.addByCopy](Materials_addByCopy.md), [Materials.item](Materials_item.md), [Materials.itemById](Materials_itemById.md), [Materials.itemByName](Materials_itemByName.md), [MeshBody.material](MeshBody_material.md), [PlasticRule.material](PlasticRule_material.md)

## Version

Introduced in version August 2014  

