
cjZfTxJgDay=2
########取成绩作废的开始、结束时间
getCjZfQsJsSj='''
select SQKSSJ,SQJSSJ from JW_CJ_CJJGLXSZB
'''
##########取年级、专业信息
getZyxxCode='''
select distinct NJDM_ID,zyh_id from JW_XJGL_XSJBXXB xsj where xsj.XJZTDM in (select XJZTDM from JW_XJGL_XJZTDMB where SFYXJ='1')
and NJDM_ID>='2015' and lower(XH )not like 's%'
'''
####取年级、专业信息下的学生信息
getNjZyXsxxCode='''
select WM_CONCat(XH) from JW_XJGL_XSJBXXB where XJZTDM in (select xjztdm from JW_XJGL_XJZTDMB where SFYXJ='1')
and NJDM_ID='{}' and ZYH_ID='{}'
group by JG_ID,NJDM_ID,ZYH_ID
'''

