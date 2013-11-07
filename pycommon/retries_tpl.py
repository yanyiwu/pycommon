#!/usr/bin/env python
#
# Copyright 2012 by Jeff Laughlin Consulting LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
 
 
from retry import retries, example_exc_handler
 
class MyException(Exception):
    pass
 
n = 0
@retries(3, hook=example_exc_handler)
def retry_me():
    global n
    n += 1
    #raise MyException('Foobar')
    a = int("a")
 
def test_retries():
    try:
        retry_me()
    except MyException, e:
        pass
    else:
        raise Exception("Failure to raise MyException")
    eq_(n, 3)
 
@retries(4, hook=example_exc_handler)
def retry_me2():
    raise BaseException()
 
def test_retries2():
    assert_raises(BaseException, retry_me2)


if __name__ == "__main__":
    try:
        retry_me()
    except Exception as err:
        print "hehe"
    print n
