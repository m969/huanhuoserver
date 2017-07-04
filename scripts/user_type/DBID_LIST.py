# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TDBIDList(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)

	def asDict(self):
		datas = []
		dct = {"values" : datas}

		for key, val in self.items():
			datas.append(val)

		return dct

	def createFromDict(self, dictData):
		for data in dictData["values"]:
			self[data] = data
		return self

class DBID_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TDBIDList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TDBIDList)

dbid_list_inst = DBID_LIST_PICKLER()