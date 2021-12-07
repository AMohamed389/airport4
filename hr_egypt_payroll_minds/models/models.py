# -*- coding: utf-8 -*-

from odoo import models, fields, api

from psycopg2.extras import NamedTupleCursor
import logging
import datedelta
from datetime import datetime
from datetime import date
_logger = logging.getLogger(__name__)

