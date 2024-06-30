import sys
import member as M
def import_guarantee()->dict:
    try:
        with open('data.txt', 'r', encoding='utf-8') as guaranteefile:
            lines = guaranteefile.read().splitlines()
            lib={}
            for line in lines:
                m = line.split('\t')
                if not m[0] is None:
                    member = M.Member(name = m[2])
                    member.record = int(m[1])
                    wechat_id = m[0]
                    lib[wechat_id] = member
            guaranteefile.close()
            return lib
    except:
        print('data.txt打开失败')
        sys.exit()