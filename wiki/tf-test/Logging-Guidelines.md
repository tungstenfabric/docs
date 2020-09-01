
1. INFO logs should ONLY be those which describe the high level test-step in a testcase. It should tell “WHAT" the test has done
1. DEBUG logs can tell "HOW” the test is being conducted. Any amount of detail can be added here
1. A single INFO log should not be printing out too much. User will mostly ignore it in such a case . (Ex : printing out a big dict)
1. A log line should always start with a capital letter 
1. Log lines should tell things that the user can understand. So, lets keep in mind that the person reading the logs would not be YOU. It would mostly be a person who has not seen that part of the test code
1. Lines like "Inside method_name" is bad
1. There should be no “print” statements in the test code. 
1. ERROR should only be shown if it there is a definite problem, not otherwise.
1. If we are repeatedly checking something in a retry loop , an ERROR log can only be shown at the end of all retries. Within a iteration, at worst, it can be a WARN.
1. Lets follow the practise that WARN logs suggest that there could be a problem, but not always. So, in cases where the test figures out that there is no problem, an INFO log should clearly refute what was logged in WARN
1. Needless to say, we should use right english grammar
1. A setUp() in a fixture should result in a single INFO log saying that the object was created. Similarly a cleanUp() should have a single INFO log telling that the object was deleted
1. Lets follow consistent style of telling status with things like 
    * "Created <Object type> <name of object> , FQ Name, UUID"
    * "Verified/Validated that xyz"
    * "Verification/Validation of xyz [passed/failed]"
    * "Deleted <object type> <name of object> , FQ Name, UUID"
1. An assert line should ALWAYS have a message to tell what failed