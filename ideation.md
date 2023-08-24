# Ideation

## Schema

Document database with mongodb or other

Useful because different schools may have different properties for their classes. Implementers should aim to use commonly used attribute names but may add their own when their colleges have features that other colleges don't.

Requirements are objects, possibly nested in each other. 
```json
{
  "type": "TYPE",
  "items": [
    ObjectId,
    "COURSE CODE",
    {
      "type": "TYPE",
      "items": [
        "COURSE CODE",
	ObjectId
      ]
    }
  ]
}
```

Requirement types:
* AND (ALL) - All requirements must be completed
* OR (ONE) - One of the requirements must be completed
* CREDITS - A provided number of credits must be completed from the group
* COUNT (n) - A provided number of courses in the group must be completed
