# ChoiceParameterValue.getChoices Method

Parent Object: [ChoiceParameterValue](ChoiceParameterValue.md)  

## Description

Method that returns the list of available choices.

## Syntax

"choiceParameterValue_var" is a variable referencing a [ChoiceParameterValue](ChoiceParameterValue.md) object.  

```python
(returnValue, names, values) = choiceParameterValue_var.getChoices()
```

## Return Value

| Type    | Description                              |
|---------|------------------------------------------|
| boolean | Returns true if the call was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| names | string\[\] | An array of the names of the choices. These coincide with the array of possible values returned by the values argument. |
| values | string\[\] | An array of the possible values. These coincide with the array of names returned by the names argument. |

## Version

Introduced in version September 2021  

