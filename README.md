These are a few simply python scripts to make running some common maven tasks easier on me.

### test.py
With no arguments, runs `mvn test` and notes all the failing tests.
If it gets a single argument, it'll use that to run `mvn test -Dtest=<arg>` and report the result.  Converts `.` to `#`, so `test.py Fixture.test` is equivalent to `mvn test -Dtest=Fixture#test`.

### checkstyle, findbugs, pmd and cpd
Each of these will run a single maven target (`checkstyle:checkstyle`, `findbugs:findbugs`, `pmd:pmd` and `pmd:cpd`, respectively) and report on the results.

### static.py
Runs each of `checkstyle.py`, `findbugs.py`, `pmd.py` and `cpd.py`, and collates and prints the results.

### deploy
Drops symlinks to the scripts so that I can save myself some typing.
