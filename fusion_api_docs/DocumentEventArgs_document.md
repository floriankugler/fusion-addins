# DocumentEventArgs.document Property

Parent Object: [DocumentEventArgs](DocumentEventArgs.md)  

## Description

Provides access to the document that is open. Can be null in the case where the event is fired before the document has been opened or after it has been closed.

## Syntax

"documentEventArgs_var" is a variable referencing a DocumentEventArgs object.  

```python
# Get the value of the property.
propertyValue = documentEventArgs_var.document
```

## Property Value

This is a read only property whose value is a [Document](Document.md).

## Version

Introduced in version August 2014  

