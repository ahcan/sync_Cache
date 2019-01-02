from Redit import Redit 
from syncDatabase.setting.Databasethomson import Database
from syncDatabase.setting import config as setting
# from syncDatabase.setting import config as settings

db = Database()

def get_job_host(index):
    host = setting.THOMSON_HOST[index]['host']
    sql = "select j.jid, p.name, w.name, j.state, j.status, j.startdate, j.enddate, w.wid, j_a.auto, p.backup from job j \
            INNER JOIN job_param p ON j.jid = p.jid and p.host = j.host and p.host = '%s'\
            INNER JOIN workflow w ON w.wid = p.wid and w.host = p.host \
            LEFT JOIN job_auto j_a ON j.jid = j_a.jid and j.host = j_a.host;"%(host)
    return db.execute_query(sql)

    # Return Json Job
def json_job_host(index):
        import time
        import json
        lstjob = get_job_host(index)
        # lstjob = [['111','huynt44','abc','Running','OK','12345','123456','2222','true','true'],['222','huynt444', 'def', 'Running','OK','12345','123456','5555','true','false']]
        args=[]
        # print len(lstjob)
        if not lstjob:
            time.sleep(1)
            lstjob = get_job_host(index)
            print "no data list job by host"
        for item in lstjob:
            JId,jobname,workflow_name,State,Status,StartDate,EndDate,workflowIdRef,backMain,isBackup = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]
            args.append({'jname'    : jobname,
                        'wid'       : workflowIdRef,
                        'wname'     : workflow_name,
                        'state'     : State,
                        'status'    : Status,
                        'jid'       : JId,
                        # 'prog'      : int(Prog),
                        'startdate' : StartDate \
                        if StartDate else None,
                        # 'ver'       : int(Ver),
                        'enddate'   : EndDate \
                        if EndDate else None,
                        'iauto'     : backMain,
                        'iBackup'  : isBackup
                })
        return json.dumps(args)

def sync_cache_job_host():
    for item in setting.REDIS_KEY:
        redis = Redit(key=item)
        val = json_job_host(setting.REDIS_KEY.index(item))
        print redis.set_data(name= setting.REDIS_NAME[0], val = val)
        # print redis.get_all()

def main():
    import time
    while True:
        sync_cache_job_host()
        time.sleep(5)

if __name__ == "__main__":
    main()