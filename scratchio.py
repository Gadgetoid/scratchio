#!/usr/bin/env python

import scratch, os, signal, imp

PLUGINS = 'plugins'
WD = os.path.dirname(os.path.realpath(__file__))
PLUGINS_DIR = os.path.join(WD, PLUGINS)

_plugins = {}

@scratch.on_message('^plugin:')
def setup_plugin(msg):
    msg = msg.split(':')
    if len(msg) == 1:
        raise ValueError("Addon not specified")
        return False
    plugin = msg[1]
    if plugin in _plugins:
        print("Plugin \"{}\" already loaded. Skipping!".format(plugin))
        return False

    plugin_path = os.path.join(PLUGINS_DIR,'{}.scratchio.py'.format(plugin))
    print("Attempting to load plugin {}".format(plugin_path))
    plugin_obj = imp.load_source('plugin_{}'.format(plugin), plugin_path)
    if hasattr(plugin_obj, 'Plugin'):
        _plugins[plugin] = getattr(plugin_obj, 'Plugin')(scratch)
        print("Load successful!")
    else:
        print("Invalid plugin format. Aborting!")

signal.pause()
