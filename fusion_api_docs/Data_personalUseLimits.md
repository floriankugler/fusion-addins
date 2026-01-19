# Data.personalUseLimits Property

Parent Object: [Data](Data.md)  

## Description

If the user is running with a "Fusion for Personal Use license", this property will return a peronalUseLimits object which provides information about file limits associated with the license. If the user is running with any other license type, this property will return null.

## Syntax

"data_var" is a variable referencing a Data object.  

```python
# Get the value of the property.
propertyValue = data_var.personalUseLimits
```

## Property Value

This is a read only property whose value is a [PersonalUseLimits](PersonalUseLimits.md).

## Version

Introduced in version May 2021  

