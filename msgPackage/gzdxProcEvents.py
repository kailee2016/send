from msgPackage import gzdxProcVar as gpv
from connectDB import gzdxDB as gd


#######更新学生绩点
def update_jd():
    if not gpv.debug:
        gd.calProc(gpv.updateXsJd,[0])
        gd.calProc(gpv.backXyyj,[0])#备份学业预警信息
        return 1
    else:
        pass
# ###更新教职工信息
# def updateAndInsert_jzg():
#     if not gpv.debug:
#         gd.calProc(gpv.updateAndinsertJzg,[0])
#         return 1
#     else:
#         pass
