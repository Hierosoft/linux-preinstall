#!/usr/bin/env python
import os

digits = "0123456789"
alphaLower = "abcdefghijklmnopqrstuvwxyz"
alphaUpper = alphaLower.upper()
to_date_flag = ".to_date.sql"

def onlyNeedles(haystack, needles):
    for h in haystack:
        if h not in needles:
            return False
    return True

def onlyLetters(haystack):
    return (onlyNeedles(haystack, alphaUpper)
            or onlyNeedles(haystack, alphaLower))

def onlyNumbers(haystack):
    return onlyNeedles(haystack, digits)

def getDateFmt(sqlVal, stripChars=None):
    if stripChars is not None:
        sqlVal = sqlVal.strip(stripChars)
    fmt = None
    if (len(sqlVal) == 9) or (len(sqlVal) == 11):
        if ((sqlVal[2] == "-") and (sqlVal[6] == "-")
                and onlyNumbers(sqlVal[0:2]) and onlyNumbers(sqlVal[7:])
                and onlyLetters(sqlVal[3:6])):
            if len(sqlVal) == 11:
                fmt = "DD-MON-YY"
            else:
                fmt = "DD-MON-YY"
    return fmt

# 08-JAN-19 (9 characters)
# 012345678

# 08-JAN-2019 (11 characters)
# 0123456789
filesReadCount = 0
filesDifferentCount = 0

def addDateConv(path):
    changedCount = 0
    ins = None
    outs = None
    try:
        ins = open(path, 'r', encoding="latin-1")
    except TypeError:  # python 2
        ins = open(path, 'r')
    outs = None
    outPath = path + to_date_flag
    try:
        outs = open(outPath, 'w', encoding="latin-1")
    except TypeError:  # python 2
        outs = open(outPath, 'w')
    originalLine = True
    global filesReadCount
    global filesDifferentCount
    lineCount = 0
    filesReadCount += 1
    done_flag = "to_date("
    while originalLine:
        originalLine = ins.readline()
        if originalLine:
            lineCount += 1
            # python2 only: unicode(originalLine, errors='replace')
            line = originalLine.rstrip()
            line2 = ""
            start = -1
            for i in range(0, len(line)):
                if start == -1:
                    if line[i] == "'":
                        start = i
                    else:
                        line2 += line[i]
                else:
                    if line[i] == "'":
                        sqlVal = line[start:i+1]
                        fmt = getDateFmt(sqlVal, stripChars="'")
                        # check for done_flag to avoid creating `to_date(to_date` recursion:
                        if (fmt is None) or (line[-len(done_flag):].lower() == done_flag):
                            line2 += sqlVal
                            # if (len(sqlVal) == 9) or (len(sqlVal) == 11):
                                # print("  NotDate: " + sqlVal)
                        else:
                            line2 += "TO_DATE(%s,'%s')" % (sqlVal, fmt)
                        start = -1
            if line != line2:
                changedCount += 1
                # print("  Converted:")
                # print("    - " + line)
                # print("    - " + line2)
                # print("")
            outs.write(line2 + "\n")
    ins.close()
    if outs is not None:
        outs.close()
        if changedCount < 1:
            os.remove(outPath)
            print("  - nothing to change so removed '" + outPath + "'")
        else:
            filesDifferentCount += 1
            print("  - wrote '" + outPath + "'")
    return changedCount, lineCount

def endsWithAny(haystack, needles, caseSensitive=True):
    for needle in needles:
        if caseSensitive:
            if sub_name[-len(needle):] == needle:
                return True
        else:
            if sub_name[-len(needle):].lower() == needle.lower():
                return True
    return False

folder_path = "."
for sub_name in os.listdir(folder_path):
    sub_path = os.path.join(folder_path, sub_name)
    if ((sub_name[:1]!=".") and os.path.isfile(sub_path)
            and (sub_name[-len(to_date_flag):] != to_date_flag)
            and endsWithAny(sub_name, [".txt", ".sql"])):
        print(sub_path + ":")

        changedCount, lineCount = addDateConv(sub_path)
        print("lineCount: " + str(lineCount))
        print("changedCount: " + str(changedCount))
print("filesReadCount: " + str(filesReadCount))
print("filesDifferentCount: " + str(filesDifferentCount))


