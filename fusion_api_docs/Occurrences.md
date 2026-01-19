# Occurrences Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to occurrences within a component and provides methods to create new occurrences.

## Methods

| Name | Description |
|----|----|
| [addByInsert](Occurrences_addByInsert.md) | Method that inserts an existing file. |
| [addExistingComponent](Occurrences_addExistingComponent.md) | Method that creates a new occurrence using an existing component. This is the equivalent of copying and pasting an occurrence in the user interface. |
| [addFromConfiguration](Occurrences_addFromConfiguration.md) | Method that inserts a configuration from a configured design. The insert will fail if the configured design being used is not from the same project as the file it is being inserted into. |
| [addNewComponent](Occurrences_addNewComponent.md) | Method that creates a new component and an occurrence that references it. |
| [addNewComponentCopy](Occurrences_addNewComponentCopy.md) | Method that creates a new occurrence by creating a new component that is a copy of an existing component. This is the equivalent of copying and using the "Paste New" command in the user interface. This is different from the addExistingComponent in that it's not a new instance to the existing component but a new component is created that has it's own definition (sketches, features, etc.) and a new occurrence instance is created to reference this new component. |
| [addNewExternalComponent](Occurrences_addNewExternalComponent.md) | Method that creates a new occurrence by creating a new external component (X-Ref) that is not saved yet. This is similar to the "New Component" command in the UI when creating an external component, where you specify a name and location but the component is created in-memory without being saved immediately. This allows programs to create and populate an external component without needing to save it first, and makes undo possible. The component will be saved automatically when the parent assembly is saved. |
| [asArray](Occurrences_asArray.md) | Get the current list of all occurrences. The occurrences are returned in the same order as they appear in the browser. |
| [classType](Occurrences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Occurrences_item.md) | Function that returns the specified occurrence using an index into the collection. |
| [itemByName](Occurrences_itemByName.md) | Returns the specified occurrence using the name of the occurrence. |

## Properties

| Name | Description |
| --- | --- |
| [asList](Occurrences_asList.md) | Returns the contents of this collection as an OccurrencesList object. This is useful when writing a function that traverses an assembly. |
| [count](Occurrences_count.md) | Returns the number of occurrences in the collection. |
| [isValid](Occurrences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Occurrences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BaseComponent.occurrences](BaseComponent_occurrences.md), [Component.occurrences](Component_occurrences.md), [FlatPatternComponent.occurrences](FlatPatternComponent_occurrences.md)

## Samples

| Name | Description |
|----|----|
| [Assembly traversal using recursion API Sample](AssemblyTraversalUsingRecursion_Sample.md) | Traverses the entire structure of the currently open assemlby using a recursive function and displays the result in a message box. This will match the occurrence structure seen in the browser. |

## Version

Introduced in version August 2014  

