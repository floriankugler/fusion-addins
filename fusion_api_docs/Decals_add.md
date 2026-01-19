# Decals.add Method

Parent Object: [Decals](Decals.md)  

## Description

Creates a new decal. Use the createInput method to first create an input object and set the available options. Then, pass that input object to the add method to create the decal.

## Syntax

"decals_var" is a variable referencing a [Decals](Decals.md) object.

```python
returnValue = decals_var.add(input)
```

## Return Value

| Type               | Description                             |
|--------------------|-----------------------------------------|
| [Decal](Decal.md) | Returns the newly created Decal object. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| input | [DecalInput](DecalInput.md) | The DecalInput object that defines the required information needed to create a new decal. A DecalInput object is the logical equivalent to the Decal command dialog by providing access to all the decal options. Passing in the DecalInput object to the add method is the equivalent of clicking the OK button on the dialog to create the decal. |

## Version

Introduced in version September 2024  

