#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

import userlogin

def main():
    if len(sys.argv) != 4:
        print 'Usage: python %s <username> <password> <realname>' % sys.argv[0]
        return
    print userlogin.new_oa_user(*sys.argv[1:])

if __name__ == '__main__':
    main()
