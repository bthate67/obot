# This file is placed in the Public Domain.

from zzz import os, sys, traceback

exc = []
skip = ["unittest"]
stopmarkers = ["ob", "python3.9"]

def called(depth=0):
    frame = sys._getframe(depth)
    try:
        filename = frame.f_back.f_code.co_filename
        plugfile = filename.split(os.sep)
        if plugfile:
            mod = []
            for i in plugfile[::-1]:
                mod.append(i)
                if i in stopmarkers:
                    break
            modstr = '.'.join(mod[::-1])[:-3]
            if 'handler_' in modstr:
                modstr = modstr.split('.')[-1]
    except AttributeError:
        modstr = None
    del frame
    return modstr

def callstack(frame):
    result = []
    loopframe = frame
    marker = ""
    while 1:
        try:
            filename = loopframe.f_back.f_code.co_filename
            plugfile = filename.split(os.sep)
            if plugfile:
                mod = []
                for i in plugfile[::-1]:
                    if i in skip:
                        continue
                    if i in stopmarkers:
                        marker = i
                        break
                    mod.append(i)
                modstr = '.'.join(mod[::-1])[:-3]

                if not modstr:
                    modstr = ".".join(plugfile)
            result.append("%s:%s" % (modstr, loopframe.f_back.f_lineno))
            loopframe = loopframe.f_back
        except AttributeError:
            break
    del frame
    return result

def where():
    return " ".join(callstack(sys._getframe(0)))

def exception(txt="", sep=" | "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if "python3" in elem[0] or "<frozen" in elem[0]:
            continue
        res = []
        for x in elem[0].split(os.sep)[::-1]:
            res.append(x)
            if x in ["ob",]:
                break
        result.append("%s %s %s" % (".".join(res[::-1]), elem[2], elem[1]))
    res = "%s | %s: %s" % (sep.join(result), exctype, excvalue)
    exc.append(res)
    del trace
    return res
