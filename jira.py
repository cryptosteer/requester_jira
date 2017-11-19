#!/usr/bin/env python3

import conf
import ingester
import logging
import json
import os
import requester

if __name__ == '__main__':

    stats = ingester.Stats()
    stats.script(conf.SCRIPT_NAME, conf.SCRIPT_VERSION, {
        'api_path': conf.API_PATH,
        'auth_user': conf.AUTH_USER,
        'site_name': conf.SITE_NAME,
        'ingester': conf.INGESTER_PATH,
        'limit': conf.LIMIT,
        'request': {
            'retries': conf.REQUEST_RETRIES,
            'timeout': conf.REQUEST_TIMEOUT,
        },
        'cache': {
            'enabled': conf.CACHE_ENABLED,
            'path': conf.CACHE_PATH,
            'seconds': conf.CACHE_SECONDS,
        },
        'log': {
            'enabled': conf.LOG_TO_FILE,
            'file': conf.LOG_FILE,
            'level': conf.LOG_LEVEL,
        },
    })

    users = requester.get_item(path='user/search?username=%')
    projects = requester.get_item(path='project')
    issues = requester.get_item(path='search?maxResults=1000')

    # Output data
    data = {
        'users': users,
        'projects': projects,
        'issues': issues,
    }

    stats.finish()
    stats.count(data)
    
    if conf.INGESTER_PATH:
        uplink = ingester.ChunkedIngesterLink(conf.INGESTER_PATH)
        uplink.chunk_dict(data)
        uplink.stats(stats)
    if conf.VERBOSE:
        data['stats'] = stats
        print(json.dumps(data, indent=4))
