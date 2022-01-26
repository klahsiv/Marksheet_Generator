def Marksheet_Generator():
    import csv
    import os

    import xlsxwriter as xlwr

    os.system('cls')
    if not os.path.exists(r"Project_App\\marksheets\\"):
        os.mkdir('Project_App\\marksheets\\')

    master_roll_path = "media//master_roll.csv"
    response_path = "media//responses.csv"
    if not os.path.exists(master_roll_path):
        print("Error")
        return
    if not os.path.exists(response_path):
        print("Error")
        return
        
    Roll_Number = {}
    with open(master_roll_path,"r") as file:
        reader = csv.reader(file)
        for line in reader:
            if line[0] != 'roll':
                Roll_Number[line[0]] = line[1]

    Stud_Responses = {}
    with open(response_path, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            if line[6] != 'Roll Number':
                Stud_Responses[(line[6]).upper()] = [line[1], line[4], line[7:]]
    
    if 'ANSWER' in Stud_Responses.keys():
        answer_key = Stud_Responses['ANSWER'][2]
    else:
        print('No Roll Number with ANSWER is present, Cannot Process!')
        return

    total_ques = len(answer_key)
    Score_List = {}
    for key, value in Roll_Number.items():
        correct = 0
        wrong = 0
        if key not in Stud_Responses:
            # print('absent')
            pass
        else:
            for i in range(total_ques):
                if Stud_Responses[key][2][i] == answer_key[i]:
                    correct += 1
                elif len(Stud_Responses[key][2][i]) != 0:
                    wrong += 1
        not_attempt = total_ques-correct-wrong
        Score_List[key] = [correct, wrong, not_attempt]
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
    # print(correct_marks, wrong_marks)
    # return
    
    
    for key, value in Roll_Number.items():
        file_path = "Project_App\\marksheets\\" + str(key) + ".xlsx"
        workbook = xlwr.Workbook(file_path)

        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'white',
            'font_size': 20,
            'underline': True,
        })

        normal_format = workbook.add_format({
            'font_size': 12,
            'align': 'right',
            'font': 'Century',
        })

        border_format = workbook.add_format({
            'border': 1,
            })

        red_format = workbook.add_format({
            'align': 'center',
            'color': 'red',
            'font_size': 12,
            'font': 'Century',
            })

        green_format = workbook.add_format({
            'align': 'center',
            'color': 'green',
            'font_size': 12,
            'font': 'Century',
            })

        blue_format = workbook.add_format({
            'align': 'center',
            'color': 'blue',
            'font_size': 12,
            'font': 'Century',
            })
        
        black_format = workbook.add_format({
            'align': 'center',
            'color': 'black',
            'font_size': 12,
            'font': 'Century',
            })

        bold_left_foramt = workbook.add_format({
            'font_size': 12,
            'align': 'left',
            'font': 'Century',
            'bold': True,
        })

        bold_center_foramt = workbook.add_format({
            'font_size': 12,
            'align': 'center',
            'font': 'Century',
            'bold': True,
        })

        worksheet = workbook.add_worksheet('quiz')
        worksheet.set_column("A:E", 17)
        worksheet.set_default_row(16)
        worksheet.set_row(4, 20)
        worksheet.insert_image('A1', 'Project_App/iitp_logo.jpg', {'x_scale': 0.8, 'y_scale': 0.8})
        worksheet.merge_range('A5:E5', 'Mark Sheet', merge_format)


        worksheet.conditional_format('A9:E12', {'type': 'cell',
                                            'criteria' : '>', 
                                            'value' : -99999999999,
                                            'format' : border_format})

        worksheet.write('A6', 'Name:', normal_format)
        worksheet.write('B6', Roll_Number[key], bold_left_foramt)
        worksheet.write('A7', 'Roll Number:', normal_format)
        worksheet.write('B7', key, bold_left_foramt)
        worksheet.write('D6', 'Exam:', normal_format)
        worksheet.write('E6', "quiz", bold_left_foramt)

        worksheet.write('B9', "correct", bold_center_foramt)
        worksheet.write('C9', "Wrong", bold_center_foramt)
        worksheet.write('D9', "Not Attempt", bold_center_foramt)
        worksheet.write('E9', "Max", bold_center_foramt)
        worksheet.write('A10', "No.", bold_center_foramt)
        worksheet.write('A11', "Marking", bold_center_foramt)
        worksheet.write('A12', "Total", bold_center_foramt)

        worksheet.write('B10', Score_List[key][0], green_format)
        worksheet.write('B11', correct_marks, green_format)
        worksheet.write('B12', Score_List[key][0] * correct_marks, green_format)

        worksheet.write('C10', Score_List[key][1], red_format)
        worksheet.write('C11', wrong_marks, red_format)
        worksheet.write('C12', Score_List[key][1] * wrong_marks, red_format)

        worksheet.write('D10', Score_List[key][2], black_format)
        worksheet.write('D11', 0, black_format)

        worksheet.write('E10', total_ques, black_format)
        final_Score_List = str(Score_List[key][0] * correct_marks + Score_List[key][1] * wrong_marks) + "/" + str(total_ques * correct_marks)
        worksheet.write('E12', final_Score_List, blue_format)

        worksheet.write('A15', "Student Ans", bold_center_foramt)
        worksheet.write('B15', "Correct Ans", bold_center_foramt)

        line = 16
        for i in range(total_ques):
            stud_line = 'A' + str(line + i)
            corr_line = 'B' + str(line + i)
            if key not in Stud_Responses:
                pass
            elif Stud_Responses[key][2][i] == answer_key[i]:
                worksheet.write(stud_line, Stud_Responses[key][2][i], green_format)
            elif len(Stud_Responses[key][2][i]) != 0:
                worksheet.write(stud_line, Stud_Responses[key][2][i], red_format)
            
            worksheet.write(corr_line, answer_key[i], blue_format)

        workbook.close()
        # break
    print("DONE")
    # print(len(Stud_Responses), len(Roll_Number))

# Marksheet_Generator()
