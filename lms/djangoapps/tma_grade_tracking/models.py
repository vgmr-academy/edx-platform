from pymongo import MongoClient


class dashboardStats():
    def __init__(self):
        self.course_id = None

    def connect(self,host,port,user=None,password=None):
        client = MongoClient(host, port)
        db = client['stat_dashboard']
        collection = db["courses"]
        return collection
    #INSERT OR UPDATE A ROW
    def add(self,collection,kwargs):
        q = {}
        check_course_id = False
        for key, value in kwargs.items():
            if key == 'course_id' and value is not None:
                check_course_id = True
        if check_course_id:
            check = self.find_by_course_id(collection,kwargs['course_id'])
            if check is None:
                collection.insert(kwargs)
                q['status'] = True
                q['action'] = 'Insert'
            else:
                for key, value in kwargs.items():
                    check[key] = value
                collection.save(check)
                q['status'] = True
                q['action'] = 'Update'
        else:
            q['status'] = False

        return q
    #FIND ONE BY COURSE_ID
    def find_by_course_id(self,collection,course_id):
        check = collection.find_one({'course_id':course_id})
        return check
    #FIND
    def find(self,collection,row=None):
        if row is not None:
            check_id = False
            for key, value in kwargs.items():
                if key == 'course_id' and value is not None:
                    check_id = True
            if check_id:
                values = collection.find(row)
            else:
                values = []
        else:
            values = collection.find()
        q = []
        for n in values:
            q.append(n)
        return q
    #ADD a new user_info
    def add_user_grade_info(self,collection,course_id,row):
        q = {}
        user_id = ''
        # check if course_id is present in current collection
        check = self.find_by_course_id(collection,course_id)
        if check is None:
            Dict = {'course_id':course_id,'users_info':{}}
            collection.insert(Dict)
            check = True
        #if course_id exist or is already created insert user_info
        if check:
            for key, value in row.items():
                if key == 'user_id':
                    user_id = value
            current = self.find_by_course_id(collection,course_id)
            if current is not None and user_id != '':
                users_info = current.get('users_info')
                if not user_id in users_info:
                    current.get('users_info')[str(user_id)] = row
                else:
                    current.get('users_info')[str(user_id)] = row
                collection.save(current)
                return True
            else:
                return False

