# ConstructionPointInput.creationOccurrence Property

Parent Object: [ConstructionPointInput](ConstructionPointInput.md)  

## Description

In order for geometry to be transformed correctly, an occurrence for creation needs to be specified when the ConstructionPoint is created based on geometry (e.g. a sketch point) in another component AND (the ConstructionPoint) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"constructionPointInput_var" is a variable referencing a ConstructionPointInput object.  

```python
# Get the value of the property.
propertyValue = constructionPointInput_var.creationOccurrence

# Set the value of the property.
constructionPointInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version August 2014  

