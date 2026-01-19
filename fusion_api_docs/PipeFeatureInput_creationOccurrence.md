# PipeFeatureInput.creationOccurrence Property

Parent Object: [PipeFeatureInput](PipeFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Pipe is created based on geometry (e.g. a path) in another component AND (the Pipe) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"pipeFeatureInput_var" is a variable referencing a PipeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = pipeFeatureInput_var.creationOccurrence

# Set the value of the property.
pipeFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version October 2023  

