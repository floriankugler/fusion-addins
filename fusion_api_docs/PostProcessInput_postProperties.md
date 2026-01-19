# PostProcessInput.postProperties Property

Parent Object: [PostProcessInput](PostProcessInput.md)  

## Description

Gets and sets the list of post properties. Each property has a string name and a ValueInput object. The default value for this is an empty NamedValues.

## Syntax

"postProcessInput_var" is a variable referencing a PostProcessInput object.  

```python
# Get the value of the property.
propertyValue = postProcessInput_var.postProperties

# Set the value of the property.
postProcessInput_var.postProperties = propertyValue
```

## Property Value

This is a read/write property whose value is a [NamedValues](NamedValues.md).

## Samples

| Name | Description |
|----|----|
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version May 2020  

