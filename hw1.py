import pymysql
import sys

# DB 접속 정보
DB_HOST = "192.168.100.20"
DB_USER = "cjulib"
DB_PASS = "security"
DB_PORT = 3306
DB_NAME = "cju"


# 1. 전체 조회 (JOIN)
def select_all():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            sql = """
            SELECT 
                m.seq,
                m.name,
                m.id,
                g.subject,
                g.score,
                g.term
            FROM member m
            JOIN grades g ON m.seq = g.member_seq
            """

            cursor.execute(sql)
            result = cursor.fetchall()

            print("\n--- [ 성적 전체 목록 ] ---")
            print("번호 | 이름(ID)        | 과목명            | 점수 | 학기")
            print("----------------------------------------------------------")

            for row in result:
                name_id = row['name'] + "(" + row['id'] + ")"

                print(f"{row['seq']:<4} | "
                      f"{name_id:<15} | "
                      f"{row['subject']:<15} | "
                      f"{row['score']:<4} | "
                      f"{row['term']}")

            print("----------------------------------------------------------")

    except pymysql.MySQLError as e:
        print("오류 발생:", e)

    finally:
        conn.close()


# 2. 성적 추가
def insert_grade():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            member_seq = input("회원번호(seq): ")
            subject = input("과목: ")
            score = input("점수: ")
            term = input("학기: ")

            sql = "INSERT INTO grades (member_seq, subject, score, term) VALUES (" + member_seq + ", '" + subject + "', " + score + ", '" + term + "')"

            print("\n[실행 쿼리]:", sql)

            cursor.execute(sql)
            conn.commit()

            print("성적 추가 완료")

    except pymysql.MySQLError as e:
        conn.rollback()
        print("오류 발생:", e)

    finally:
        conn.close()


# 3. 성적 삭제
def delete_grade():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            num = input("삭제할 성적 번호(id): ")

            sql = "DELETE FROM grades WHERE id = " + num

            print("\n[실행 쿼리]:", sql)

            cursor.execute(sql)
            conn.commit()

            print("삭제 완료")

    except pymysql.MySQLError as e:
        conn.rollback()
        print("오류 발생:", e)

    finally:
        conn.close()


# 4. 성적 수정
def update_grade():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            num = input("수정할 성적 번호(id): ")
            score = input("새 점수: ")

            sql = "UPDATE grades SET score = " + score + " WHERE id = " + num

            print("\n[실행 쿼리]:", sql)

            cursor.execute(sql)
            conn.commit()

            print("수정 완료")

    except pymysql.MySQLError as e:
        conn.rollback()
        print("오류 발생:", e)

    finally:
        conn.close()


# 메인 메뉴
def main_menu():
    while True:
        print("\n--- [ 성적 관리 시스템 ] ---")
        print("1. 전체조회")
        print("2. 성적 추가")
        print("3. 성적 삭제")
        print("4. 성적 수정")
        print("5. 종료")
        print("---------------------------")

        choice = input("메뉴 선택: ")

        if choice == '1':
            select_all()
        elif choice == '2':
            insert_grade()
        elif choice == '3':
            delete_grade()
        elif choice == '4':
            update_grade()
        elif choice == '5':
            print("프로그램 종료")
            break
        else:
            print("잘못된 입력")


# 실행
if __name__ == "__main__":
    main_menu()