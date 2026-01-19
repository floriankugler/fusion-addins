# Occurrences.addNewComponentCopy Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Method that creates a new occurrence by creating a new component that is a copy of an existing component. This is the equivalent of copying and using the "Paste New" command in the user interface. This is different from the addExistingComponent in that it's not a new instance to the existing component but a new component is created that has it's own definition (sketches, features, etc.) and a new occurrence instance is created to reference this new component.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.addNewComponentCopy(component, transform)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the newly created occurrence or null if the creation failed. The newly created component can be obtained by using the component property of the returned Occurrence. |

## Parameters

| Name | Type | Description |
|----|----|----|
| component | [Component](Component.md) | The existing component to create a copy of. |
| transform | [Matrix3D](Matrix3D.md) | A transform that defines the location for the new occurrence |

## Version

Introduced in version September 2022  

