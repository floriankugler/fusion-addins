# Document.name Property

Parent Object: [Document](Document.md)  

## Description

This property gets and sets the name of the document. You can only set the name of a document before the document is saved for the first time. You can use the isSaved property to determine this. If the document has not been saved and the name is changed, the specified name will be the default name shown in the Save dialog, which the user can modify before saving the document.  

If the file has been saved, this property behaves as read-only. Setting the name will fail because the name is controlled by the DataFile associated with this document. However, you can edit the name of the DataFile, which you can obtain by using the dataFile property of the document.

## Syntax

"document_var" is a variable referencing a Document object.  

```python
# Get the value of the property.
propertyValue = document_var.name

# Set the value of the property.
document_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version August 2014  

