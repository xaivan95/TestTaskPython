"""Система генерации различных версий ПО по шаблону"""
from .config_parser import ConfigParser
from .version_generator import VersionGenerator
from .version_filter import VersionSorter, VersionFilter, VersionFormatter
from .validator import ConfigValidator, VersionValidator

__version__ = "1.0.0"
