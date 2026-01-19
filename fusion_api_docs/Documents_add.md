# Documents.add Method

Parent Object: [Documents](Documents.md)  

## Description

Creates and opens a new document of the specified type.

## Remarks

Creating a document is not supported within any of the Command related events. When a command is running, a transaction is open, and creating and closing documents cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"documents_var" is a variable referencing a [Documents](Documents.md) object.

```python
# Uses no optional arguments.
returnValue = documents_var.add(documentType)

# Uses optional arguments.
returnValue = documents_var.add(documentType, visible, options)
```

## Return Value

| Type                     | Description                  |
|--------------------------|------------------------------|
| [Document](Document.md) | Returns the created document |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| documentType | [DocumentTypes](DocumentTypes.md) | A value from the DocumentTypes enum that specifies the type of document to create. |
| visible | boolean | Optional argument specifying is the document should be visible or not. Currently, documents can only be created visibly so this argument must always be true. This is an optional argument whose default value is True. |
| options | [NamedValues](NamedValues.md) | Various options that are supported that are specific to the document type. See the documentation for the DocumentTypes enum for information about the options supported for the various types. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version November 2014  

