# ValidateInputsEventArgs.areInputsValid Property

Parent Object: [ValidateInputsEventArgs](ValidateInputsEventArgs.md)  

## Description

Used with AreInputsValid event to specify if the all of the inputs for the command are valid or not. If you set this to false, indicating they are not valid, the OK button for the dialog is disabled forcing the user to correct the inputs before continuing. If you set this to true the OK button will be enabled, as long as the inputs satisfy their own requirements. For example, if a SelectionCommandInput is defined to have at minimum number of entities selected, that requirement must be met, or if a ValueCommandInput has an invalid value specified, the OK button will still be disabled.

## Syntax

"validateInputsEventArgs_var" is a variable referencing a ValidateInputsEventArgs object.  

```python
# Get the value of the property.
propertyValue = validateInputsEventArgs_var.areInputsValid

# Set the value of the property.
validateInputsEventArgs_var.areInputsValid = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

