# DrawingDocument.creationId Property

Parent Object: [DrawingDocument](DrawingDocument.md)  

## Description

Returns the creation ID of this document. When a new document is created, Fusion assigns it a creation ID that will remain constant for the life of the document. The ID that is assigned is unique. However, it's possible that more than one document can have the same ID. This happens in the case where a document is copied. In this case a new document is created but an existing document is copied. It's only when a new document is created that a creation ID is generated and assigned.  

Using this ID can be useful in cases where the save of a new document is started and you can use this ID to match the completion of the save operation on the cloud to the original document.

## Syntax

"drawingDocument_var" is a variable referencing a DrawingDocument object.  

```python
# Get the value of the property.
propertyValue = drawingDocument_var.creationId
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2022  

