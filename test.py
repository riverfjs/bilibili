from fun_mysql import AccessToMysql

limit_count = 5
mysqlInfo = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '123456',
    'db': 'stuclassdb',
    'port': 3306,
    'charset': 'utf8mb4'
}


def main():
    tt = AccessToMysql(host=mysqlInfo['host'], user=mysqlInfo['user'], passwd=mysqlInfo['passwd'],
                       database=mysqlInfo['db'])
    StudentSql = "CREATE TABLE Student " \
                 "(Sno char(9) PRIMARY KEY," \
                 "Sname char(10)," \
                 "Ssex char(4)," \
                 "Sage char(3)," \
                 "Sdept char(3))" \
                 "DEFAULT charset='utf8mb4';"
    CourseSql = "CREATE TABLE Course" \
                "(Cno char(2) PRIMARY KEY," \
                "Cname char(10)," \
                "Cpno char(2)," \
                "Ccredit char(2))" \
                "DEFAULT charset='utf8mb4';"
    SCSql = "CREATE TABLE SC" \
            "(Sno char(9) PRIMARY KEY," \
            "Cno char(2)," \
            "Grade char(3))" \
            "DEFAULT charset='utf8mb4';"
    tt.execute_sql(StudentSql)
    print("student ok")
    tt.execute_sql(CourseSql)
    print("course ok")
    tt.execute_sql(SCSql)
    print("sc ok")


def insertdata():
    tt = AccessToMysql(host=mysqlInfo['host'], user=mysqlInfo['user'], passwd=mysqlInfo['passwd'],
                       database=mysqlInfo['db'])
    Student = []
    Course = []
    SC = []
    # print("Student Data")
    # for ii in range(0, 4):
    #     Sno, Sname, Ssex, Sage, Sdept = input("").split(" ")
    #     tmp = (Sno, Sname, Ssex, Sage, Sdept)
    #     StudentSql = "INSERT INTO Student (Sno, Sname, Ssex, Sage, Sdept) VALUE {}".format(tmp)
    #     tt.execute_sql(StudentSql)
    #     print(tmp, "ok")
    #     Student.append(tmp)
    # print(Student)

    # print("Course Date")
    # for ii in range(0, 7):
    #     Cno, Cname, Cpno, Ccredit = input("").split(" ")
    #     tmp = (Cno, Cname, Cpno, Ccredit)
    #     CourseSql = "INSERT INTO Course (Cno, Cname, Cpno, Ccredit) VALUE {}".format(tmp)
    #     tt.execute_sql(CourseSql)
    #     print(tmp, "ok")
    #     Course.append(tmp)
    # print(Course)

    print("SC Date")
    for ii in range(0, 5):
        Sno, Cno, Grade = input("").split(" ")
        tmp = (Sno, Cno, Grade)
        SCSql = "INSERT INTO SC (Sno, Cno, Grade) VALUE {}".format(tmp)
        tt.execute_sql(SCSql)
        print(tmp, "ok")

        SC.append(tmp)
    print(SC)


if __name__ == '__main__':
    # main()
    insertdata()
