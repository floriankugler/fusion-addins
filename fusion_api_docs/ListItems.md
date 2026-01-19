# ListItems Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the list of items in a check box list. This object supports the ability to add items to the list and iterate through the existing items.

## Methods

| Name | Description |
|----|----|
| [add](ListItems_add.md) | Adds a new item to the list. |
| [addSeparator](ListItems_addSeparator.md) | Adds a separator to the list. This is not supported for button rows. |
| [classType](ListItems_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](ListItems_clear.md) | Clears all of the items from the list. |
| [item](ListItems_item.md) | Returns the specified check box list item using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](ListItems_count.md) | Gets the number of items in the collection. |
| [isValid](ListItems_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ListItems_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ButtonRowCommandInput.listItems](ButtonRowCommandInput_listItems.md), [DropDownCommandInput.listItems](DropDownCommandInput_listItems.md), [ListControlDefinition.listItems](ListControlDefinition_listItems.md), [RadioButtonGroupCommandInput.listItems](RadioButtonGroupCommandInput_listItems.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2015  

