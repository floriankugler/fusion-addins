# TriadCommandInput.lastChangeMade Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Returns which value was most recently changed. To determine the actual change made you need to compare the transforms returned by the transform and lastTransform properties. Having information about the specific type of change made makes it easier to compare the matrices because you know what to look for.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.lastChangeMade
```

## Property Value

This is a read only property whose value is a [TriadChanges](TriadChanges.md).

## Version

Introduced in version May 2022  

