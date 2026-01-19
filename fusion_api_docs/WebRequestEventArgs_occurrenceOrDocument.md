# WebRequestEventArgs.occurrenceOrDocument Property

Parent Object: [WebRequestEventArgs](WebRequestEventArgs.md)  

## Description

Used during the insertedFromURL or openedFromURL events and returns the Document (openedFromURL) or Occurrence (insertedFromURL) that was just created.

## Syntax

"webRequestEventArgs_var" is a variable referencing a WebRequestEventArgs object.  

```python
# Get the value of the property.
propertyValue = webRequestEventArgs_var.occurrenceOrDocument
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version May 2016  

