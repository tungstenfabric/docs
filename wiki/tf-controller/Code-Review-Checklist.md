## Important aspects while performing code review/submission

* Is there any upgrade implication? If so at a minimum need
  + tag on bug
  + tools to address it
  + documentation on impact (tag it as release-note in bug)
* Is there any change in schema? If so
  + make sure fields aren't removed (can comment as deprecated)
  + make sure fields are defined at end (to ensure that if constructors were called without
    named parameters old code will still work)