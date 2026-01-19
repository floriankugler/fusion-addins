# PostProcessInput.areToolChangesMinimized Property

Parent Object: [PostProcessInput](PostProcessInput.md)  

## Description

Gets and sets that operations may be reordered between setups to minimize the number of tool changes. Operations within each setup will still be executed in the programmed order. This is commonly used for tombstone machining where you have multiple setups. The default value for this property is false.

## Syntax

"postProcessInput_var" is a variable referencing a PostProcessInput object.  

```python
# Get the value of the property.
propertyValue = postProcessInput_var.areToolChangesMinimized

# Set the value of the property.
postProcessInput_var.areToolChangesMinimized = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2016  

