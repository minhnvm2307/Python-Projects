import numpy as np

class student:
    def __init__(self, ID : int, fullname: str, date_of_birth: str, GPA: float):
        self.ID = ID
        self.fullname = fullname
        self.date_of_birth = date_of_birth
        self.GPA = GPA
    
    def __str__(self):
        return("Student information:\n"
              + "- ID: " + str(self.ID) + "\n"
              + "- Fullname: " + self.fullname + "\n"
              + "- Date of birth: " + self.date_of_birth + "\n"
              + "- GPA: " + str(self.GPA) + "\n")


def students_to_file():
    try:
        file = open("test.txt", "w")
        print("Ghi file:")

        for i in range(3):
            # Array contain full information of a student (4 elements)
            stu_info = input("Nhap thong tin sinh vien (ID, fullname, dob, gpa): ").split(' ')
            student_i = student(int(stu_info[0]), stu_info[1], stu_info[2], float(stu_info[3]))

            file.write(student_i.__str__())

        file.close()
    except (Exception):
        print("Error", Exception)
    finally:
        print("Finish writing process!")

arr = np.array([], dtype=float)
for i in range(10):
    arr = np.append(arr, int(i))

print(arr)