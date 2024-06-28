import tkinter
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calc_bmi(h,w):
    bmi = round(w/h**2*10)/10
    if bmi < 18.5:
        result = 'Underweight'
    elif bmi < 25:
        result = 'Normal'
    elif bmi < 30:
        result = 'Overweight'
    else:
        result = 'Obese'
    return bmi, result
def save_data():
    try:
        name = nameentry.get()
        age = ageentry.get()
        height = heightentry.get()
        weight = weightentry.get()
        if name == "" or age == "" or height == "" or weight == "":
            tkinter.messagebox.showwarning("Error. Missing data.", "All fields are required.")
        elif not age.isnumeric() or not height.isnumeric() or not weight.isnumeric():
            tkinter.messagebox.showwarning("Error. Invalid data.", "Age, height and weight must be a number.")
        elif int(age)<0 or int(age)>110:
            tkinter.messagebox.showwarning("Error. Incorrect data.", "Age must be from 1 to 110.")
        elif int(height)<50 or int(height)>300:
            tkinter.messagebox.showwarning("Error. Incorrect data.","Height must be from 50 to 300cm.")
        elif int(weight)<2 or int(weight)>600:
            tkinter.messagebox.showwarning("Error. Incorrect data.", "Weight must be from 2 to 600kg.")
        else:
            bmi = calc_bmi(int(height)/100, int(weight))
            with open('bmis.txt', 'a') as fwrite:
                fwrite.write(f"{name} {age} {height} {weight} {bmi[0]} {bmi[1]}\n")
            bmi_var.set(bmi[0])
            result_var.set(bmi[1])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def show_chart():
    try:
        bmis={'Underweight':0, 'Overweight':0, 'Obese':0, 'Normal':0}
        with open('bmis.txt', 'r') as bmisfile:
            for line in bmisfile:
                res=line.split()
                bmis[res[5]]+=1

        labels=[]
        nums=[]
        for lab,num in bmis.items():
            if num!=0:
                labels.append(lab)
                nums.append(num)

        fig = Figure(figsize=(4, 4), dpi=100)
        plot = fig.add_subplot(111)
        plot.pie(nums, radius=1, labels=labels, autopct='%1.1f%%', shadow=True, rotatelabels=True)
        canvas = FigureCanvasTkAgg(fig, chartframe)
        canvas.get_tk_widget().grid(row=1, column=0, padx=15, pady=15)
    except FileNotFoundError:
        messagebox.showerror("Error", "No BMI details found. Save some details first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

window = tkinter.Tk()
window.title('BMI Calculator')

frame = tkinter.Frame(window, pady=15, padx=15)
frame.pack(padx=50,pady=20)

userinfoframe = tkinter.LabelFrame(frame, text="User Information", pady=10, padx=10)
userinfoframe.grid(row=0, column=0, padx=15)

chartframe = tkinter.LabelFrame(frame, text="BMI Chart", pady=10, padx=10)
chartframe.grid(row=0, column=1, padx=15)

namelabel = tkinter.Label(userinfoframe, text="Name", pady=5)
nameentry = tkinter.Entry(userinfoframe,width=20)
namelabel.grid(row=0, column=0)
nameentry.grid(row=0, column=1)

agelabel = tkinter.Label(userinfoframe, text="Age", pady=5)
ageentry = tkinter.Entry(userinfoframe,width=20)
agelabel.grid(row=1, column=0)
ageentry.grid(row=1, column=1)

heightlabel = tkinter.Label(userinfoframe, text="Height (сm)", pady=5)
heightentry = tkinter.Entry(userinfoframe, width=20)
heightlabel.grid(row=2, column=0)
heightentry.grid(row=2, column=1)

weightlabel = tkinter.Label(userinfoframe, text="Weight (kg)", pady=5)
weightentry = tkinter.Entry(userinfoframe, width=20)
weightlabel.grid(row=3, column=0)
weightentry.grid(row=3, column=1)

savebtn=tkinter.Button(userinfoframe,text="Save",command=save_data, width=20)
savebtn.grid(row=4,column=1, padx=15, pady=15)

resultframe = tkinter.LabelFrame(userinfoframe, text="BMI result", pady=10, padx=10)
resultframe.grid(row=5, column=1, padx=15, pady=15)

bmi_var=tkinter.StringVar()
bmi_output = tkinter.Label(resultframe, font=("Arial",25), textvariable=bmi_var)
bmi_output.grid(row=0,column=0)

result_var=tkinter.StringVar()
output = tkinter.Label(resultframe, textvariable=result_var)
output.grid(row=1,column=0)

chartbtn = tkinter.Button(chartframe,text="Show chart",command=show_chart, width=20)
chartbtn.grid(row=0,column=0)

window.mainloop()
