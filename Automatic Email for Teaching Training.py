from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import date
from datetime import datetime
import time
import smtplib # for Hyperlink
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Initialize WebDriver
driver = webdriver.Chrome()  # or specify the path to your WebDriver


# ------------------------ Part 2 : Get into Course Data Website --------------------------------

# Directly go into the course link
driver.get("https://tcs.edb.gov.hk/tcs/publicCalendar/start.htm")
print('\n\t\t\t\t [Resize Window]\n')
driver.set_window_size(1600,1000)
courseSession = driver.find_element(By.CLASS_NAME, "home-section2")
courseSession = courseSession.find_element(By.LINK_TEXT, "Secondary School")
courseSession.click()

# Translate to Chinese
print('\t\t\t\t [Translate to Chinese]\n')
transToChinese = driver.find_element(By.LINK_TEXT, "中")
transToChinese.click()

# Filter
print('\t\t\t\t [Filtering]\n')
filter = driver.find_element(By.LINK_TEXT,"更多選項")
filter.click()
leveltype = Select(driver.find_element(By.ID,"leveltype"))
leveltype.select_by_visible_text('中學')

financeType = Select(driver.find_element(By.ID,"financeType"))
financeType.select_by_visible_text('資助')

search = driver.find_element(By.ID,"search")
search.click()

# ----------------------- Part 3 : Extract Data ----------------------------

# Locate the table element
print('\t\t\t\t [Get courses]\n')
courses = driver.find_elements(By.CLASS_NAME,"divTableRow")

# Iterate through rows
outputData_all = []
outputData_newT= []
today = date.today().strftime("%Y/%m/%d")
### today = "2024/02/29"

# count how many course today
print('\t\t\t\t [Mathching...]\n')
counter = 0
for data in courses:
    date = data.find_element(By.CLASS_NAME,"divTableCell").text
    if date == today:
        counter += 1
        # Extract data from specific columns

        courseNo = data.find_element(By.TAG_NAME,"a").text
        print("CourseNo   ", counter, ": ", courseNo)

        dataTitle = data.find_elements(By.CLASS_NAME,"divTableCell")

        # Case 1: Only for New Teachers (Core)
        dataInsideCourseID = dataTitle[1]
        teacherTag = dataInsideCourseID.find_element(By.TAG_NAME,"form")
        hrefList = teacherTag.find_elements(By.TAG_NAME,"a")
        # There should be only 1 <a href> tag with the name "新教師 (核心)" 
        if len(hrefList) == 1:
            if hrefList[0].text == f'新教師\n(核心)':

                courseName = dataTitle[3].text
                print("CourseName ", counter, ": ", courseName,"\n\t*newT Only",f"\n")
                outputData_newT.append([courseNo,courseName])
            # Case 2: for all teachers
            else:
                courseName = dataTitle[3].text
                print("CourseName ", counter, ": ", courseName,f"\n")
                outputData_all.append([courseNo,courseName])
        else:
                courseName = dataTitle[3].text
                print("CourseName ", counter, ": ", courseName,f"\n")
                outputData_all.append([courseNo,courseName])

### print(outputData_newT)
### print(outputData_all)

#------------ Part 4 : Send email through Gmail  ---------------------
# To login with SMTP, you have to change the security setting of your gmail account,
# Refer to this acticle: https://medium.com/seaniap/%E5%A6%82%E4%BD%95%E7%94%A8-pyhon-%E5%AF%84%E9%9B%BB%E5%AD%90%E9%83%B5%E4%BB%B6-1-%E4%BD%BF%E7%94%A8smtplib-gmail-cbf40e592c52
# The email will be automatically sent with SMTP

today = datetime.today().strftime("%d/%m")
msg = MIMEMultipart()
msg['From']     = ""
#msg['To']     = ""
msg['To']     = "" # for testing
msg['Subject']  = f"教育局培訓活動一覽表 ({today})"

# Create table_1 (for all teachers) in HTML style
tableForAllTeacher = ""
counterTemp = 0
for course in outputData_all:
     tableForAllTeacher += f'''
     <tr>
        <td style="border: 1px solid black; border-collapse: collapse;"><a href=\"https://tcs.edb.gov.hk/tcs/admin/courses/previewCourse/forPortal.htm?courseId={outputData_all[counterTemp][0]}&lang=zh\">{outputData_all[counterTemp][0]}</a></td>
        <td style="border: 1px solid black; border-collapse: collapse;">{outputData_all[counterTemp][1]}</th>
     </tr>
     '''
     counterTemp += 1

# Create table_2 (for new teachers only) in HTML style
if outputData_newT:
    tableForNewTeacherOnly = ""
    counterTemp = 0
    for course in outputData_newT:
        tableForNewTeacherOnly += f'''
        <tr>
            <td style="border: 1px solid black; border-collapse: collapse;"><a href=\"https://tcs.edb.gov.hk/tcs/admin/courses/previewCourse/forPortal.htm?courseId={outputData_all[counterTemp][0]}&lang=zh\">{outputData_all[counterTemp][0]}</a></td>
            <td style="border: 1px solid black; border-collapse: collapse;">{outputData_newT[counterTemp][1]}</td>
        </tr>
        '''
        counterTemp += 1
    tableForNewTeacherOnly = f"<table style=\"font-size:20px; border: 1px solid black; border-collapse: collapse;\">{tableForNewTeacherOnly}</table><br>"
else:
    tableForNewTeacherOnly = "無"




message = f'''<p style="font-size:20px;">各位同工：<br><br>

以下為教育局培訓活動一覽表 ({today}) 供同工參考，同工如有需要，可於 e-services 報讀課程，並聯絡 <b> 副校長</b>。謝謝！<br><br>

(Teddy 代行)<br><br>
———————————————————————————<br><br>
<b><i>一﹑全部課程／活動</i></b><br></p>
<table style="font-size:20px; border: 1px solid black; border-collapse: collapse;">{tableForAllTeacher}</table><br>

<p style="font-size:20px;"><b><i>二﹑新教師 (核心)</i></b></p>
<div style="font-size:20px">{tableForNewTeacherOnly}</div>


<p style="font-size:20px;"><b><i>三﹑資訊科技教育 專業發展課程</i></b><br>
http://www.edb.gov.hk/tc/edu-system/primary-secondary/applicable-to-primary-secondary/it-in-edu/pdp-ited.html</p>'''
msg.attach(MIMEText(message,"html"))




mailserver = smtplib.SMTP('smtp.gmail.com',587)
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login("account", "passwork")
mailserver.sendmail("sender@email.com","receiver@email.com",msg.as_string())
mailserver.quit()







print("\n\t\t\t\t[Automation Finish]\n\n")
print("\t\t The email is successfully sent. Thank you.")
time.sleep(3)


# Close the browser
driver.quit()