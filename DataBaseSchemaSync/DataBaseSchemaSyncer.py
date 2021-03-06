#!/usr/bin/python
# -*- coding: UTF-8 -*-
from _mysql import OperationalError
import sys
import os
from DataBaseSchemaSync.SchemaComparison import SchemaComparison

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataBaseSchemaSync.db.MysqlDataBaseConnector import MysqlDataBaseConnector
import json
from DataBaseSchemaSync.util.configer import Configer
import sys


class DataBaseSchemaSyncer(object):
    def __init__(self, conf_path=None):
        try:
            configure = Configer(conf_path)
        except IOError:
            sys.stderr.write('file not exist')
            sys.exit(1)

        self.db = json.loads(configure.get_config())

        try:
            self.source = MysqlDataBaseConnector(self.db['source'])
        except OperationalError:
            sys.stderr.write('database connect error')
            sys.exit(1)

        try:
            self.target = MysqlDataBaseConnector(self.db['target'])
        except OperationalError:
            sys.stderr.write('database connect error')
            sys.exit(1)

        self.source.fetch()
        self.target.fetch()
        self.compare()

    def compare(self):
        mcmp = SchemaComparison(self.source, self.target)
        diffs = mcmp.compare(self.source.database, self.target.database)
        mcmp.sync(diffs)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        DataBaseSchemaSyncer()
    else:
        DataBaseSchemaSyncer(sys.argv[1])


