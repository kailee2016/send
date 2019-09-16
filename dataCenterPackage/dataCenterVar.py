
debug=False #是否开同步启调试模式
headers={'HTTP_DC_SECRECT':'','charsets':'utf-8'}
############数据中心分配###############
headers['HYYP_DC_SECRECT']='hJ5kBRuV'#网络中心分配
name='JWXT'#数据中心分配
token='chst9Fgk'#网络中心分配
baseUrl='http://dapi.gzhu.edu.cn:8012/datacenter/core/cpi'
urlDir={'tch':'/hUolEw8l'}#同步目录
########page_count:默认每页数据,page_index:起始页
page_count=300


params={'name':name,'token':token,'page_count':page_count}


#同步之前先备份
backUpExists='''
select nvl(count(*),0) from all_tables where table_name=upper('jw_jg_jzgxxb_back')
'''
dropBackUpTable='''
drop table jw_jg_jzgxxb_back
'''
backUpCode='''
create table jw_jg_jzgxxb_back as (select * from jw_jg_jzgxxb)
'''
###可以将以下事务封装为数据库的存储过程
updateAndinsertJzg='LIKAI_JW_PUBLICINTERFACE.UPDATEANDINSERTJZG'
