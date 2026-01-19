# ShellFeatureInput.creationOccurrence Property

Parent Object: [ShellFeatureInput](ShellFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the shell is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the shell) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"shellFeatureInput_var" is a variable referencing a ShellFeatureInput object.  

```python
# Get the value of the property.
propertyValue = shellFeatureInput_var.creationOccurrence

# Set the value of the property.
shellFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version November 2014  

