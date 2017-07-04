# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *
import space_data


def onBaseAppReady(isBootstrap):
    """
    KBEngine method.
    baseapp已经准备好了
    @param isBootstrap: 是否为第一个启动的baseapp
    @type isBootstrap: BOOL
    """
    INFO_MSG('onBaseAppReady: isBootstrap=%s, appID=%s, bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
             (isBootstrap, os.getenv("KBE_COMPONENTID"), os.getenv("KBE_BOOTIDX_GROUP"),
              os.getenv("KBE_BOOTIDX_GLOBAL")))
    if isBootstrap:
        KBEngine.createBaseLocally("SpacesManager", {})
        # KBEngine.createBaseFromDBID("BigWorld", 1, _onBigWorldCreateCB)
        # KBEngine.executeRawDatabaseCommand("SELECT * from mini_Spaces", _dbCmdSelectCB)


def _onSpacesManagerCreateCB(resultCollect, num, errorInfo):
    DEBUG_MSG("_onSpacesManagerCreateCB")
    pass


def _dbCmdSelectCB(resultCollect, num, errorInfo):
    DEBUG_MSG(resultCollect)
    DEBUG_MSG(num)
    # DEBUG_MSG(errorInfo)
    if errorInfo is not None:
        DEBUG_MSG("error")
        KBEngine.executeRawDatabaseCommand(
            "CREATE TABLE mini_Spaces (name VARCHAR(255) NOT NULL DEFAULT '' primary key, dbid BIGINT)",
            _dbCmdCreateTblCB)
    else:
        DEBUG_MSG("not error")
        if not resultCollect:
            DEBUG_MSG("resultCollect == []")
            bigWorld = KBEngine.createBaseLocally("BigWorld", {})
            if bigWorld:
                DEBUG_MSG("create bigWorld success")
                bigWorld.writeToDB(_bigWorldSavedCB)
                # KBEngine.executeRawDatabaseCommand("INSERT INTO mini_Spaces VALUES ('BigWorld', 0)",
                # _dbCmdInsertBigWorldCB)
            else:
                ERROR_MSG("create bigWorld failed")
        else:
            for value in resultCollect:
                if value[0] == b'BigWorld':
                    DEBUG_MSG("==b")
                    if value[1] != 0:
                        KBEngine.createBaseFromDBID("BigWorld", int(value[1].decode('ascii')), _onBigWorldCreateCB)
                        DEBUG_MSG(int(value[1].decode('ascii')))
                        return


def _onBigWorldCreateCB(baseRef, dbid, wasActive):
    if baseRef is None:
        DEBUG_MSG("_onBigWorldCreateCB-failed")
        KBEngine.executeRawDatabaseCommand("SELECT * from mini_Spaces", _dbCmdSelectCB)
        # KBEngine.executeRawDatabaseCommand("INSERT INTO MiniGame.tbl_BigWorld VALUES(0,0,0,0,0,0,0,0,0)", _dbCmdCB)
    else:
        DEBUG_MSG("_onBigWorldCreateCB-success")


def _dbCmdCreateTblCB(resultCollect, num, errorInfo):
    DEBUG_MSG(errorInfo)
    if errorInfo is None:
        bigWorld = KBEngine.createBaseLocally("BigWorld", {})
        if bigWorld:
            DEBUG_MSG("create bigWorld success")
            bigWorld.writeToDB(_bigWorldSavedCB)
            # KBEngine.executeRawDatabaseCommand("INSERT INTO mini_Spaces VALUES ('BigWorld', 0)",
            # _dbCmdInsertBigWorldCB)
        else:
            ERROR_MSG("create bigWorld failed")
    else:
        ERROR_MSG("create tbl failed")


def _bigWorldSavedCB(success, bigWorld):
    DEBUG_MSG("")
    KBEngine.executeRawDatabaseCommand("INSERT INTO mini_Spaces VALUES ('BigWorld', " + str(bigWorld.databaseID) + ")",
                                       _dbCmdInsertBigWorldCB)


def _dbCmdInsertBigWorldCB(resultCollect, num, errorInfo):
    DEBUG_MSG(errorInfo)


def _dbCmdCB(resultCollect, num, errorInfo):
    if resultCollect is None:
        DEBUG_MSG("_dbCmdCB-resultCollect is None.")
        DEBUG_MSG(errorInfo)
    else:
        DEBUG_MSG("_dbCmdCB-resultCollect is not None.")
        DEBUG_MSG(resultCollect)
        # KBEngine.createBaseFromDBID("BigWorld", 1, _onBigWorldCreateCB)
    pass


def onReadyForLogin(isBootstrap):
    """
    KBEngine method.
    如果返回值大于等于1.0则初始化全部完成, 否则返回准备的进度值0.0~1.0。
    在此可以确保脚本层全部初始化完成之后才开放登录。
    @param isBootstrap: 是否为第一个启动的baseapp
    @type isBootstrap: BOOL
    """
    return 1.0


def onBaseAppShutDown(state):
    """
    KBEngine method.
    这个baseapp被关闭前的回调函数
    @param state: 0 : 在断开所有客户端之前
                  1 : 在将所有entity写入数据库之前
                  2 : 所有entity被写入数据库之后
    @type state: int
    """
    INFO_MSG('onBaseAppShutDown: state=%i' % state)


def onInit(isReload):
    """
    KBEngine method.
    当引擎启动后初始化完所有的脚本后这个接口被调用
    @param isReload: 是否是被重写加载脚本后触发的
    @type isReload: bool
    """
    INFO_MSG('onInit::isReload:%s' % isReload)


def onFini():
    """
    KBEngine method.
    引擎正式关闭
    """
    INFO_MSG('onFini()')


def onCellAppDeath(addr):
    """
    KBEngine method.
    某个cellapp死亡
    """
    WARNING_MSG('onCellAppDeath: %s' % (str(addr)))


def onGlobalData(key, value):
    """
    KBEngine method.
    globalData有改变
    """
    DEBUG_MSG('onGlobalData: %s' % key)


def onGlobalDataDel(key):
    """
    KBEngine method.
    globalData有删除
    """
    DEBUG_MSG('onDelGlobalData: %s' % key)


def onGlobalBases(key, value):
    """
    KBEngine method.
    globalBases有改变
    """
    DEBUG_MSG('onGlobalBases: %s' % key)


def onGlobalBasesDel(key):
    """
    KBEngine method.
    globalBases有删除
    """
    DEBUG_MSG('onGlobalBasesDel: %s' % key)


def onLoseChargeCB(ordersID, dbid, success, datas):
    """
    KBEngine method.
    有一个不明订单被处理， 可能是超时导致记录被billing
    清除， 而又收到第三方充值的处理回调
    """
    DEBUG_MSG('onLoseChargeCB: ordersID=%s, dbid=%i, success=%i, datas=%s' % \
              (ordersID, dbid, success, datas))
