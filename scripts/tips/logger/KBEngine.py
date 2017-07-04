def onRequestCharge( ordersID, entityDBID, datas ):
	"""	
	功能说明：
	当请求计费时（通常是baseapp上调用了KBEngine.charge），该回调被调用。
	可在此函数内数据进行检查和修改，将最终结果通过KBEngine.chargeResponse提交给引擎。
	
	注意：该回调接口必须实现在入口模块(kbengine_defs.xml->entryScriptFile)中。
	
	
	参数：
	
	
	@ordersID
	uint64，订单的ID。
	
	
	@entityDBID
	uint64，提交订单的实体DBID。
	
	
	@datas
	bytes，客户端请求时所附带的数据，可将数据转发第三方平台。
	
	
	
	
	
	
	版权归KBEngine所有。
	

	"""
	pass

def addTimer( initialOffset, repeatOffset=0, callbackObj ):
	"""	
	功能说明：
	注册一个定时器，定时器由回调函数callbackObj触发，回调函数将在"initialOffset"秒后被执行第1次，而后将每间隔"repeatOffset"秒执行1次。
	
	例子:
	
	# 这里是使用addTimer的一个例子
	        import KBEngine
	 
	        # 增加一个定时器，5秒后执行第1次，而后每1秒执行1次，用户参数是9
	        KBEngine.addTimer( 5, 1, onTimer_Callbackfun )
	 
	        # 增加一个定时器，1秒后执行，用户参数缺省是0
	        KBEngine.addTimer( 1, onTimer_Callbackfun )
	 
	    def onTimer_Callbackfun( id ):
	        print "onTimer_Callbackfun called: id %i" % ( id )
	        # if 这是不断重复的定时器，当不再需要该定时器的时候，调用下面函数移除:
	        #     KBEngine.delTimer( id )
	
	
	
	参数：
	
	
	@initialOffset
	float，指定定时器从注册到第一次回调的时间间隔（秒）。
	
	
	@repeatOffset
	float，指定第一次回调执行后每次执行的时间间隔（秒）。必须用函数delTimer移除定时器，否则它会一直重复下去。值小于等于0将被忽略。
	
	
	@callbackObj
	function，指定的回调函数对象。
	
	
	
	
	
	返回:
	
	integer，该函数返回timer的内部id，这个id可用于delTimer移除定时器。
	
	
	
	
	
	

	"""
	pass

def delTimer( id ):
	"""	
	功能说明：
	函数delTimer用于移除一个注册的定时器，移除后的定时器不再执行。只执行1次的定时器在执行回调后自动移除，不必要使用delTimer移除。
	如果delTimer函数使用一个无效的id（例如已经移除），将会产生错误。
	
	到KBEngine.addTimer参考定时器的一个使用例子。
	
	
	参数：
	
	
	@id
	integer，它指定要移除的定时器id。
	
	
	
	
	
	
	
	

	"""
	pass

def onLoggerAppReady(  ):
	"""	
	功能说明：
	当前进程已经准备好的时候回调此函数。
	注意：该回调接口必须实现在入口模块(kbengine_defs.xml->entryScriptFile)中。
	
	
	

	"""
	pass

def onLoggerAppShutDown(  ):
	"""	
	功能说明：
	进程关闭会回调此函数。
	注意：该回调接口必须实现在入口模块(kbengine_defs.xml->entryScriptFile)中。
	
	
	

	"""
	pass

def onLogWrote( datas ):
	"""	
	功能说明：
	如果这个函数在脚本中有实现，logger进程获得了一条新日志，该回调函数被调用。
	数据库接口在kbengine_defs.xml->dbmgr->databaseInterfaces定义。
	
	注意：该回调接口必须实现在入口模块(kbengine_defs.xml->entryScriptFile)中。
	
	
	参数：
	
	
	@datas
	bytes，日志数据。
	
	
	
	
	
	

	"""
	pass

