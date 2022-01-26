
def concise_marksheet_generator():

    import os
    import csv

    os.system('cls')
    if not os.path.exists(r"Project_App\\marksheets\\"):
        os.mkdir('Project_App\\marksheets')
    
    if os.path.exists('Project_App/marksheets/concise_marksheet.csv'):
        os.remove('Project_App/marksheets/concise_marksheet.csv')

    master_roll_path = "media//master_roll.csv"
    response_path = "media//responses.csv"
    if not os.path.exists(master_roll_path):
        print("Error")
        return
    if not os.path.exists(response_path):
        print("Error")
        return

    Roll_Number = {}
    with open(master_roll_path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[0] != 'roll':
                Roll_Number[line[0]] = line[1]

    Stud_Responses = {}
    with open(response_path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[6] != 'Roll Number':
                Stud_Responses[(line[6]).upper()] = [line[0], line[1], line[2], line[3], line[4], line[5], line[7:]]

    if 'ANSWER' in Stud_Responses.keys():
        answer_key = Stud_Responses['ANSWER'][6]
    else:
        print('No Roll Number with ANSWER is present, Cannot Process!')
        return

    total_ques = len(answer_key)

    correct_marks = 5
    wrong_marks = -1
    if os.path.exists("Project_App/marks.csv"):
        with open("Project_App/marks.csv", "r") as file:
            reader = csv.reader(file)
            # print(reader)
            for line in reader:
                # print(line)
                correct_marks = float(line[0])
                wrong_marks = float(line[1])
                break

    Score_List = {}

    header_for_answers=[]
    for i in range(total_ques):
        header_for_answers.append('Unnamed: '+ str(7+i))

    header_for_answers.append('statusAns')
    header = ['Timestamp', 'Email address', 'Google_Score', 'Name', 'IITP webmail', 'Phone (10 digit only)','Final_Score','Roll Number']
    header.extend(header_for_answers)

    for key, value in Roll_Number.items():
        right = 0
        wrong = 0
        if key not in Stud_Responses:
            pass
        else:
            for i in range(total_ques):
                if Stud_Responses[key][6][i] == answer_key[i]:
                    right += 1
                elif len(Stud_Responses[key][6][i]) != 0:
                    wrong += 1
        not_attempted = total_ques-right-wrong
        Score_List[key] = [right, wrong, not_attempted]

        pos_marks = correct_marks*right
        final_marks = correct_marks*right + wrong_marks*wrong

        Google_Score = str(pos_marks) + "/" + str(total_ques*correct_marks)
        Final_Score = str(final_marks) + "/" + str(total_ques*correct_marks)

        if key not in Stud_Responses:
            concise_info = ['', '', "ABSENT", Roll_Number[key], '', '', "ABSENT", key]
        else:
            concise_info = [Stud_Responses[key][0], Stud_Responses[key][1],
                            Google_Score, Stud_Responses[key][3], 
                            Stud_Responses[key][4], Stud_Responses[key][5], 
                            Final_Score, key]
        
        concise_info.extend(Stud_Responses[key][-1])
        concise_info.append(Score_List[key])

        if os.path.exists('Project_App/marksheets/concise_marksheet.csv'):
            with open('Project_App/marksheets/concise_marksheet.csv', 'a', newline='') as file:
                writer=csv.writer(file)
                writer.writerow(concise_info)
                file.close()
        else:
            with open('Project_App/marksheets/concise_marksheet.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerow(concise_info)
                file.close()
        
    print("DONE")


# concise_marksheet_generator()
