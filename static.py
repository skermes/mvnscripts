#! /usr/bin/python3

import findbugs
import checkstyle
import pmd
import cpd
import out

import itertools
import os.path

if __name__ == '__main__':
    import sys

    bugFound, styleChecked, pmdRan, dupChecked = findbugs.runTarget(), checkstyle.runTarget(), \
                                                 pmd.runTarget(), cpd.runTarget()
    out.printlns('', '')

    if not bugFound:
        print(out.banner(out.red('FIND BUGS TARGET FAILED')))

    if not styleChecked:
        print(out.banner(out.red('CHECK STYLE TARGET FAILED')))

    if not pmdRan:
        print(out.banner(out.red('PMD TARGET FAILED')))

    if not dupChecked:
        print(out.banner(out.red('CODE DUPLICATION TARGET FAILED')))

    if not any([bugFound, styleChecked, pmdRan, dupChecked]):
        sys.exit()

    problems = itertools.chain(findbugs.bugsFound(),
                               checkstyle.checkstyleProblems(),
                               pmd.pmdViolations(),
                               cpd.duplications())

    noProblems = True
    for srcFile, problemgroup in itertools.groupby(sorted(problems), lambda x: x[0]):
        out.printlns('', os.path.relpath(srcFile), '-' * 79)
        for _, line, message in problemgroup:
            line = str(line)
            print(out.red(line), '-', message)

        noProblems = False

    if noProblems:
        print(out.banner(out.green('NO STATIC ANALYSIS PROBLEMS')))
