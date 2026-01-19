# ChoiceProperty.getChoices Method

Parent Object: [ChoiceProperty](ChoiceProperty.md)  

## Description

Method that returns the list of available choices.

## Syntax

"choiceProperty_var" is a variable referencing a [ChoiceProperty](ChoiceProperty.md) object.  

```python
(returnValue, names, choices) = choiceProperty_var.getChoices()
```

## Return Value

| Type    | Description                              |
|---------|------------------------------------------|
| boolean | Returns true if the call was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| names | string\[\] | An array of the names of the choices. These coincide with the array of choices returned by the choices argument. |
| choices | string\[\] | An array of the choices. These coincide with the array of names returned by the names argument. |

## Version

Introduced in version August 2014  

