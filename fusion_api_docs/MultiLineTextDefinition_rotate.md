# MultiLineTextDefinition.rotate Method

Parent Object: [MultiLineTextDefinition](MultiLineTextDefinition.md)  

## Description

Rotates the text box.

## Syntax

"multiLineTextDefinition_var" is a variable referencing a [MultiLineTextDefinition](MultiLineTextDefinition.md) object.

```python
# Uses no optional arguments.
returnValue = multiLineTextDefinition_var.rotate(angle)

# Uses optional arguments.
returnValue = multiLineTextDefinition_var.rotate(angle, keyPoint)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| angle | double | The angle to rotate the text, specified in radians. |
| keyPoint | [TextBoxKeyPoints](TextBoxKeyPoints.md) | The key point the rotation is defined around. This is optional and defaults the center of the text box. This is an optional argument whose default value is TextBoxKeyPoints.MiddleTextBoxKeyPoint. |

## Version

Introduced in version December 2020  

