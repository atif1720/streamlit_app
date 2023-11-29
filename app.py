
import streamlit as st
import plotly.express as px
import pandas as pd
import time
import os
import shutil
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
# import pyautogui
from selenium.webdriver.common.alert import Alert
from datetime import datetime

st.set_page_config(page_title="Veriflow Automation", layout="wide")

def app():

    # Display the image
    st.image("Dataflow.png", use_column_width=False, width=200)
    st.markdown('<style>div.block-container{padding-top:2rem; padding-left: 1rem;}</style>', unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color:dark orange;'>Automation Testing : Veriflow Portal</h1>", unsafe_allow_html=True)

    # Define category colors for both pie chart and bar chart
    category_colors = {
        'Total Cases': '#FF0000',
        'Cases Completed': '#00FF00',
    }

    # Function to create a pie chart
    def create_pie_chart(data):
        # Use a categorical color palette to prevent label color changes
        fig = px.pie(data, values='value', names='category', title="Pie Chart", hole=0.5, color=category_colors)
        return fig

    # Function to create a bar chart
    def create_bar_chart(data):
        fig = px.bar(data, x='category', y='value', color="category", title="Bar Chart", barmode="group")
        return fig

    # Creating an empty dataframe
    df = pd.DataFrame()

    col1, col2 = st.columns(2)

    # File Uploader 1
    with col1:
        uploaded_file_1 = st.file_uploader("Upload CSV - Validation Data(FQC)", type=["csv"])
        if uploaded_file_1 is not None:
            df = pd.read_csv(uploaded_file_1)
            st.write("Uploaded CSV File 1:")

    # File Uploader 2
    with col2:
        uploaded_file_2 = st.file_uploader("Upload CSV - Document Mapping", type=["csv"])
        if uploaded_file_2 is not None:
            df_moe = pd.read_csv(uploaded_file_2)
            st.write("Uploaded CSV File 2:")

    ## Sign In function
    def sign_in():
        username = driver.find_element(By.ID, 'username')
        username.send_keys('Anmol_Chadha')
        time.sleep(2)
        pwd = driver.find_element(By.ID, 'password')
        pwd.send_keys('Veriflow@123')
        time.sleep(2)
        submit_button = driver.find_element(By.CLASS_NAME, 'submit-text')
        submit_button.click()
        print("login done")

    ## Initiate case Function
    def initiate_case():
        version = df['VERSION'][i]
        print(version)
        ## CLicking on the Initiate case Camera Icon
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[11]/div[1]/div/div[2]/a")))
    #     title_value = "Initiate Case 8"
    #     element = driver.find_element(By.CSS_SELECTOR, f'[title="{title_value}"]')
    #     element.click()
        element_initiate_case = driver.find_elements(By.CLASS_NAME, 'icon-service')
        element_initiate_case[9].click()
        
        ## Initiating the version of the case
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[11]/div[2]/div/div/div[4]/a")))
        element_version = driver.find_element(By.PARTIAL_LINK_TEXT, version)
        element_version.click()  
        print("done")

    ## data Entry
    def data_entry():
        global barcode
        error = []
        name=df['APPLICANTFIRSTNAME'][i]
        middle=df['APPLICANTMIDDLENAME'][i]
        middle_name = df['APPLICANTMIDDLENAME'][i]
        last=df['APPLICANTLASTNAME'][i]
        customer = df['CUSTOMER'][i]
        package_name = df['PACKAGE'][i]
        middle_name_new = str(middle_name)
        passport_number=df['PASSPORTCURRENTNO'][i]
        passport_country = df['PASSPORT_ISSUING_COUNTRY_ID'][i]
        passport_expiry=df['PASSPORT_EXPIRY_DATE'][i]
        gender=df['GENDER'][i]
        country=df['COUNTRY_OF_BIRTH'][i]
        Nationality=df['NATIONALITY'][i]
        dob=df['DATEOFBIRTH'][i]
        Email_id=df['Email_ID'][i]
        date_format = '%d/%m/%Y'
        dob_dateformat = datetime.strptime(dob, date_format)
        passport_expiry_dateformat = datetime.strptime(passport_expiry, date_format)
        wait = WebDriverWait(driver, 120) 
        
        iframe_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cshsTaskWindow')))
        driver.switch_to.frame(iframe_element)

        #selecting customer  
        wait = WebDriverWait(driver, 120)
        dropdown = wait.until(EC.visibility_of_element_located((By.ID, "combo_div_3")))
        Select(dropdown).select_by_visible_text(customer)
        
        time.sleep(4)
        # custom selecting GP dentist 
        wait = WebDriverWait(driver, 120)
        dropdown = wait.until(EC.visibility_of_element_located((By.ID, "combo_div_12")))
        Select(dropdown).select_by_visible_text(package_name)
        time.sleep(3)

        # Entering the Name
        first_name=driver.find_element(By.ID, 'input_div_13_1_1_1_1_1_1')
        first_name.send_keys(name)
        if len(middle_name_new) != 3:
            print("middle name exist")
            print(middle_name)
            middle_name_blank=driver.find_element(By.ID, 'input_div_13_1_1_1_2_1_1')
            middle_name_blank.send_keys(middle_name)

        last_name=driver.find_element(By.ID, "input_div_13_1_1_1_3_1_1")
        last_name.send_keys(last)

        if len(middle_name_new) != 3:
            print("middle name exist")
            print(middle_name)
        middle_name_blank=driver.find_element(By.ID, 'input_div_13_1_1_1_2_1_1')
        middle_name_blank.send_keys(middle_name)   
        
        # Entering Passport Number
        passport_num=driver.find_element(By.ID, 'input_div_13_1_4_1_2_1_1')
        passport_num.send_keys(passport_number)
        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'input_div_21'))))
            
        # Entering DOB
        date_of_birth=driver.find_elements(By.ID, 'input_div_21')
        date_of_birth[0].send_keys(dob) 

        # Selecting Passport Country
        passport =Select(driver.find_element(By.ID, 'combo_div_18'))
        passport.select_by_visible_text(passport_country)
        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_div_17']")))) 
            
        # Entering Passport Expiry Date
        expiry=driver.find_element(By.ID, 'input_div_17')
        expiry.send_keys(passport_expiry)

        ## Selecting Gender, DOB, Nationality and E-mail ID
        gender_dropdown =Select (driver.find_element(By.ID, 'combo_div_16'))
        gender_dropdown.select_by_visible_text(gender)

        birth_country=Select (driver.find_element(By.ID, 'combo_div_23'))
        birth_country.select_by_visible_text(country)

        nationality=Select(driver.find_element(By.ID, 'combo_div_24'))
        nationality.select_by_visible_text(Nationality)

        time.sleep(3)

        email_id=driver.find_element(By.ID, 'input_div_13_1_13_1_1_1_1')
        email_id.send_keys(Email_id)
        
        ## CLicking ont he Proceed & confirm Button
        proceed_click = driver.find_element(By.XPATH, "//*[@id='div_1_1_2_1_2_1_1']/div/button")
        proceed_click.click()
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='div_1_1_9']/div/button")))
        confirm_click = driver.find_element(By.XPATH, "//*[@id='div_1_1_9']/div/button")
        confirm_click.click()
        
        ## Extracting barcode
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, 'div_2_2_3')))
        output_value = driver.find_element(By.ID, 'div_1_1_1_1_1')
        out_str =output_value.text
        time.sleep(5)
        barcode = out_str.split("'")[1].strip()
        print(barcode)
        barcode_dict.update({'new_barcode':barcode})
        

        
        ## CLicking the Continue Button
        continue_next = driver.find_element(By.XPATH, "//*[@id='div_2_2_1']/a")
        continue_next.click()
        child = driver.window_handles[0]
        # Switch to newly opened window
            
        driver.switch_to.window(child)
        time.sleep(2)
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='div_1_2_1_1']/div/div/div/div[2]/div[2]")))
        return barcode

    ## Education Check IA
    def educational_check_ia():
        applicant_name_as_document = df['APPLICANTSNAMEASPERDOCUMENT_LHS'][i]
        qualification_att = df['QUALIFICATIONATTAINED_LHS'][i]
        qual_confered_date_ia = df['QUALIFICATIONCONFERREDDATE_LHS'][i]
        date_forma_excel = df['CONFERREDDATEFORMAT_LHS'][i]
        college_name = df['COLLEGEORINSTITUTIONNAME_LHS'][i]
        education_type = df['QUALIFICATIONTYPE_LHS'][i]
        degree_completed = df['COMPLETEDDEGREEORCOURSE_LHS'][i]
        IA_name_edu = df["IA_Name_education"][i]
        required_ia_code = int(df['IA_CODE_ED'][i])
        ia_name_eductaion = df['IA_NAME_ED_LHS'][i]
        dob=df['DATEOFBIRTH'][i]
        date_format = '%d/%m/%Y'
        dob_dateformat = datetime.strptime(dob, date_format)
        qual_confered_date_ia_dateformat = datetime.strptime(qual_confered_date_ia, date_format)
        
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='combo_div_8']/option[3]")))

        #selecting customer
        pay_meth = driver.find_element(By.XPATH, "//*[@id='combo_div_8']/option[3]")
        pay_meth.click()
        
        # Scroll the window by 30%
        scroll_percentage = 20
        script = f"window.scrollBy(0, window.innerHeight * {scroll_percentage/100});"
        driver.execute_script(script)
        
        nextloop = True
        while nextloop:
            ia_search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/input")
            ia_search.send_keys(ia_name_eductaion)
            #edit_12345
            time.sleep(20)
            ia_code= driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr/td[1]")
            ia_list=[]
            for c in range(len(ia_code)):
                if ia_code[c].text == str(required_ia_code):
                    print(c)
                    ia_list.append(c)
                else:
                    pass
            if len(ia_list) == 0:
                ia_search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/input")
                ia_search.click()
                ia_search.send_keys(Keys.CONTROL,'a')
                ia_search.send_keys(Keys.BACKSPACE)
                nextloop=True
                
            else:
                
                b = ia_list[0]
                ia_check = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[9]/div/button".format(b+1)
                ia_find = driver.find_element(By.XPATH, ia_check)
                ia_find.click()
                nextloop = False
                


        time.sleep(7)
    #     IA_name_edu = df["IA_Name_education"][i]
    #     driver.find_element(By.ID, "input_div_5_1_8_1_2_1_1_r0").send_keys(IA_name_edu)
        app_name = driver.find_element(By.ID, "input_div_5_1_14_1_3_1_1_r0")
        app_name.send_keys(applicant_name_as_document)
        qual_attained = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[12]/div[2]/div/div/div[3]/div/div/div/div/div/input")
        qual_attained.send_keys(qualification_att)
        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_div_25_r0']"))))
        qual_att = driver.find_element(By.XPATH, "//*[@id='input_div_25_r0']")
        qual_att.send_keys(qual_confered_date_ia)

        time.sleep(5)
        pyautogui.moveTo(550, 460)
        time.sleep(1)
        pyautogui.click(button="left")
        time.sleep(5)
        college_fill = driver.find_element(By.ID, "input_div_5_1_14_1_1_1_1_r0")
        college_fill.send_keys(college_name)
        education_fill = driver.find_element(By.ID, 'combo_div_16')
        education_fill.send_keys(education_type)
        deg_compfill = driver.find_element(By.ID, 'combo_div_17')
        deg_compfill.send_keys(degree_completed)
        date_format = driver.find_element(By.ID, 'combo_div_26')
        date_format.send_keys(date_forma_excel)
        time.sleep(3)
        mode_of_studyfill = driver.find_element(By.ID, 'combo_div_19')
        mode_of_studyfill.send_keys("NA")
        

        
    ## Employment check IA
    def employment_check_ia():
        last_profile = df['LASTPROFILEORDESIGNATION_LHS'][i]
        nature_employment = df['NATUREOFEMPLOYMENT_LHS'][i]
        middle_name = df['APPLICANTMIDDLENAME'][i]
        emp_from=df['EMPLOYMENTPERIODFROM_LHS'][i]
        emp_to=df['EMPLOYMENTPERIODTO_LHS'][i]
        emp_from_format=df['EMPLOYMENTPERIODFROMFORMAT_LHS'][i]
        emp_to_format=df['EMPLOYMENTPERIODTOFORMAT_LHS'][i]
        middle_name_new = str(middle_name)
        employment_ia_name = df['IA_Name_employment'][i]
        required_ia_code_em = int(df['IA_CODE_EM'][i])
        ia_name_employment = df['IA_NAME_EM_LHS'][i]

        date_format = '%d/%m/%Y'
        dob_dateformat = datetime.strptime(dob, date_format)
        emp_from_dateformat = datetime.strptime(emp_from, date_format)
        emp_to_dateformat = datetime.strptime(emp_to, date_format)
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='combo_div_8']/option[3]")))

        #selecting customer
        pay_meth = driver.find_element(By.XPATH, "//*[@id='combo_div_8']/option[3]")
        pay_meth.click()
        time.sleep(3)
        nextloop = True
        while nextloop:
            ia_search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[4]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/input")
            ia_search.send_keys(ia_name_employment)
            time.sleep(20)
            ia_code= driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[4]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr/td[1]")
            ia_list=[]
            print(len(ia_code))
            for c in range(len(ia_code)):
    #             print(ia_code[i].text)
                if ia_code[c].text == str(required_ia_code_em):
                    print(c)
                    ia_list.append(c)
                else:
                    pass
            print(ia_list)
            if len(ia_list) == 0:
                ia_search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[4]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/input")
                ia_search.click()
                ia_search.send_keys(Keys.CONTROL,'a')
                ia_search.send_keys(Keys.BACKSPACE)
                nextloop=True
                
            else:
                
                b = ia_list[0]
                ia_check = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[4]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[9]/div/button".format(b+1)
                ia_find = driver.find_element(By.XPATH, ia_check)
                ia_find.click()
                nextloop = False

        time.sleep(7)
        employ_ia_name = driver.find_element(By.ID, "input_div_5_1_6_1_2_1_1_r0")
        employ_ia_name.send_keys(employment_ia_name)
        
        employ_ia_name_loc = driver.find_element(By.ID, "input_div_5_1_6_1_2_1_1_r0")
        if len(employ_ia_name_loc.get_attribute("value")) == 0:
            employ_ia_name_loc.send_keys(employment_ia_name)
        else:
            pass
        
        last_profile_emp = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[10]/div[2]/div/div/div[3]/div/div/div/div/div/input")
        last_profile_emp.send_keys(last_profile)
        nature_of_emp = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[11]/div[2]/div/div/div[1]/div/div/div/div/div/select')
        nature_of_emp.send_keys(nature_employment)

        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_div_13_r0']"))))

        emp_from_date = driver.find_element(By.XPATH, "//*[@id='input_div_13_r0']")
        emp_from_date.send_keys(emp_from)
        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_div_15_r0']"))))

        emp_to_date = driver.find_element(By.XPATH, "//*[@id='input_div_15_r0']")
        emp_to_date.send_keys(emp_to)
        time.sleep(5)
        pyautogui.moveTo(550, 460)
        time.sleep(1)
        pyautogui.click(button="left")

        emp_from_format_date = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[12]/div[2]/div/div/div[3]/div/div/div/div/div/div/select")
        emp_from_format_date.send_keys(emp_from_format)
        time.sleep(2)
        emp_to_format_date = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[13]/div[2]/div/div/div[1]/div/div/div/div/div/div/select")
        emp_to_format_date.send_keys(emp_to_format)
        time.sleep(1)
        department = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[11]/div[2]/div/div/div[2]/div/div/div/div/div/input')
        department.send_keys('Not Available')
        emp_employmentapplicant_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[20]/div[2]/div/div/div[3]/div/div/div/div/div/input")
        emp_employmentapplicant_name.send_keys(applicant_name_as_document)
            
        next_ia = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[7]/div[2]/div/div/div[6]/div/div/div/button")
        next_ia.click()

    def good_standing_ia():
        cgs_reg1 = df['GS_LICENSENUMBER_LHS'][i]
        cgs_reg2 =df['GS_LICENSENUMBER_LHS'][i]
        cgs_prof_qual = df['GS_PROFESSIONALQUALIFICATIONNAME_LHS'][i]
        cgs_emplo_iss = df['GS_DOCUMENTISSUEDATE_LHS'][i]
        cgs_lic_status = df['GS_LICENCESTATUS_LHS'][i]
        cgs_emplo_exp = df['GS_LICENSEEXPIRYDATE_LHS'][i]
        cgs_expo_form=df['GS_LICENSEEXPIRYDATEFORMAT_LHS'][i]
        cgs_impo_form=df['GS_DOCUMENTISSUEDATEFORMAT_LHS'][i] 
        ia_name_goodstanding = df['IA_NAME_CGS_LHS'][i]
        gd_ia_name = df['IA_Name_gd'][i]
        required_ia_code_gs = int(df['IA_CODE_GS'][i])
        ia_name_goodstanding = df['IA_NAME_CGS_LHS'][i]
        applicant_name_as_document = df['APPLICANTSNAMEASPERDOCUMENT_LHS'][i]
        date_format = '%d/%m/%Y'
        dob_dateformat = datetime.strptime(dob, date_format)
        cgs_emplo_iss_dateformat = datetime.strptime(cgs_emplo_iss, date_format)
        cgs_emplo_exp_dateformat = datetime.strptime(cgs_emplo_exp, date_format)
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='combo_div_8']/option[3]")))

        
        #selecting customer
        pay_meth = driver.find_element(By.XPATH, "//*[@id='combo_div_8']/option[3]")
        pay_meth.click()
        
        time.sleep(4)
        nextloop = True
        while nextloop:
            ia_search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[5]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/input")
            ia_search.send_keys(ia_name_goodstanding)
            #edit_12345
            time.sleep(50)
            ia_code= driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr/td[1]")
            ia_list=[]
            print(len(ia_code))
            for c in range(len(ia_code)):
    #             print(ia_code[i].text)
                if ia_code[c].text == str(required_ia_code_gs):
                    print(c)
                    ia_list.append(c)
                else:
                    pass
            print(ia_list)
            if len(ia_list) == 0:
                ia_search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[5]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/input")
                ia_search.click()
                ia_search.send_keys(Keys.CONTROL,'a')
                ia_search.send_keys(Keys.BACKSPACE)
                nextloop=True
                
            else:
                
                b = ia_list[0]
                ia_check = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[9]/div/button".format(b+1)
                ia_find = driver.find_element(By.XPATH, ia_check)
                ia_find.click()
                nextloop = False

        time.sleep(7)
        gs_reg_no_ia_1 = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[13]/div[2]/div/div/div[1]/div/div/div/div/div/input")
        
    #     gd_ia_name_loc = driver.find_element(By.ID, "input_div_5_1_7_1_2_1_1_r0")
    #     if len(gd_ia_name_loc.get_attribute("value")) == 0:
    #         gd_ia_name_loc.send_keys(gd_ia_name)
    #     else:
    #         pass
        
        if isinstance(cgs_reg1, float):
            gs_reg_no_ia_1.send_keys(int(cgs_reg1))
        else:
            gs_reg_no_ia_1.send_keys(int(cgs_reg1))
        
        gs_reg_no_ia_2 = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[14]/div[2]/div/div/div[1]/div/div/div/div/div/input")
        
        if isinstance(cgs_reg2, float):
            gs_reg_no_ia_2.send_keys(int(cgs_reg2))
        else:
            gs_reg_no_ia_2.send_keys(int(cgs_reg2))
        
        applicant_gs_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[14]/div[2]/div/div/div[2]/div/div/div/div/div/input")
        applicant_gs_name.send_keys(applicant_name_as_document)
        prof_qualification_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[13]/div[2]/div/div/div[2]/div/div/div/div/div/input")
        prof_qualification_name.send_keys(cgs_prof_qual)
        time.sleep(1)
        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[14]/div[2]/div/div/div[3]/div/div/div/div/div/input"))))

        cgs_emp_issue = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[14]/div[2]/div/div/div[3]/div/div/div/div/div/input")
        cgs_emp_issue.send_keys(cgs_emplo_iss)

        lic_sta_val = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[11]/div[2]/div/div/div[3]/div/div/div/div/div/select")
        lic_sta_val.send_keys(cgs_lic_status)
        time.sleep(1)
        driver.execute_script("arguments[0].removeAttribute('readonly')", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[12]/div[2]/div/div/div[1]/div/div/div/div/div/input"))))

        cgs_emp_exp = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[12]/div[2]/div/div/div[1]/div/div/div/div/div/input")
        cgs_emp_exp.send_keys(cgs_emplo_exp)
        time.sleep(3)
        
        doc_cfs_iss_format = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[15]/div[2]/div/div/div[1]/div/div/div/div/div/div/select")
        doc_cfs_iss_format.send_keys(cgs_impo_form)

        exp_cgs_format = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[5]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[12]/div[2]/div/div/div[3]/div/div/div/div/div/div/select")
        exp_cgs_format.send_keys(cgs_expo_form)
    
        next_ia = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[7]/div[2]/div/div/div[6]/div/div/div/button")
        next_ia.click()
                  

    def upload_map_ia():
    #     driver.refresh()
        print('1')
        global b
        payment_mode = df['PAYMENT_MODE'][i]
        check_edu=df['QUALIFICATIONATTAINED_LHS'][i]
        check_emp=df['LASTPROFILEORDESIGNATION_LHS'][i]
        check_licen=df['REGNORLICENCENUMBERORID_LHS'][i]
        check_good=df['GS_PROFESSIONALQUALIFICATIONNAME_LHS'][i]
        name=df['APPLICANTFIRSTNAME'][i]
        
        driver.switch_to.frame(2)
        print('2')

        wait = WebDriverWait(driver, 120)
        element_payment_method = wait.until(EC.element_to_be_clickable((By.ID, 'collapseHeader_div_10')))
        element_payment_method.click()
        print('3')
            
        # Selecting the Credit Card as MOP(Mode of Payment) 
        wait = WebDriverWait(driver, 120)
        dropdown = wait.until(EC.visibility_of_element_located((By.ID, 'combo_div_11')))
        Select(dropdown).select_by_visible_text(payment_mode)
        
        j_error = upload_map_ia_testing()

        # CLicking on Add Button
        wait = WebDriverWait(driver, 120)
        add_product = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'BPMButton')))
        add_product.click()


        ## Checking and Clicking on the Check-Box of Add-Products
        if pd.isna(check_edu):
            print('not educational check')
        else:
            print('Its an educational check')
            components = driver.find_elements(By.XPATH ,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
            for a in range(len(components)):
                components = driver.find_elements(By.XPATH ,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
                component = components[a].text
                if component == "Education":
                    click_comp = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr[{}]/td[4]/div/div/div[2]/label/input".format(a+1)
                    click_component = driver.find_element(By.XPATH, click_comp)
                    click_component.click()
                else:
                    pass

        time.sleep(2)
        if pd.isna(check_emp):
            print('not employment check')
        else:
            print('Its an employment check')
            components = driver.find_elements(By.XPATH , "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
            for a in range(len(components)):
                components = driver.find_elements(By.XPATH ,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
                component = components[a].text
                if component == "Employment":
                    click_comp = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr[{}]/td[4]/div/div/div[2]/label/input".format(a+1)
                    click_component = driver.find_element(By.XPATH, click_comp)
                    click_component.click()
                else:
                    pass

        time.sleep(2)
        if pd.isna(check_licen):
            print('not license check')
        else:
            print('Its a license check')
            components = driver.find_elements(By.XPATH ,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
            for a in range(len(components)):
                components = driver.find_elements(By.XPATH ,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
                component = components[a].text
                if component == "Health License":
                    click_comp = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr[{}]/td[4]/div/div/div[2]/label/input".format(a+1)
                    click_component = driver.find_element(By.XPATH, click_comp)
                    click_component.click()
                else:
                    pass

        time.sleep(2)
        if pd.isna(check_good):
            print('Not in good standing check')
        else:
            print("It's a good standing check")

            component_found = False 

            while not component_found:
                components = driver.find_elements(By.XPATH ,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div")
                for a in range(len(components)):
                    component = components[a].text
                    if component == "Certificate of Good Standing":
                        click_comp = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/table/tbody/tr[{}]/td[4]/div/div/div[2]/label/input".format(a+1)
                        click_component = driver.find_element(By.XPATH, click_comp)
                        click_component.click()
                        component_found = True
                        break  

                if not component_found:
                    time.sleep(4)
                    click_next_page = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[4]/div[2]/div/ul/li[4]/a")
                    click_next_page.click()
                    time.sleep(2)
        time.sleep(6)
        save_ph = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[9]/div/div/div/div[2]/div/div/div/div/div/div[6]/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/div/div[3]/div/div/div[2]/div/div/div[2]/div/button")
        save_ph.click()
        time.sleep(5)
        applicant_name = name 
        df_new = df_map[df_map['Applicant Name'].str.contains(applicant_name)].reset_index()
        new_subbarcode = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[10]/div/div/div/div/div[2]/div/div/div/div")
        subbarcodes = new_subbarcode.text
        print(subbarcodes)
        barcode_dict.update({'new_subbarcodes':subbarcodes})
        print(barcode_dict)
        time.sleep(2)
        b = new_subbarcode.text.count('\n') + 1

        df_new = df_map[df_map['Applicant Name'].str.contains(applicant_name)].reset_index()
    #     file_name = df_new['Document Name'][i]
        print(len(df_new))
        for a in range(len(df_new)):
            file_location = df_new['Upload File'][a]
            file_name = df_new['Document Name'][a]
            wait = WebDriverWait(driver, 30)
            element_browser = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='abc']/fieldset/span")))
            element_browser.click()
            time.sleep(5)
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(file_location)
            time.sleep(2)
            driver.switch_to.default_content()
            time.sleep(2)
            pyautogui.press('esc')

            wait = WebDriverWait(driver, 300) 
            iframe_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cshsTaskWindow')))
            driver.switch_to.frame(iframe_element)

            wait = WebDriverWait(driver, 30)
            element_upload = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='submit']")))
            element_upload.click()
            WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[3]/button")))


            insert_new = driver.find_element(By.CLASS_NAME, "btn.addDataTableRow.span12")
            driver.execute_script("arguments[0].click();", insert_new)
            print('value of a is:', a)
            time.sleep(2)
            if a>4:
                name_one = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[1]/div/div/div/div/select".format(a-4)
                map_name = Select(driver.find_element(By.XPATH, name_one))
                time.sleep(7)

                map_name.select_by_visible_text(file_name)
                check_one = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[2]/div/div/div/div/select".format(a-4)
                check_type = Select(driver.find_element(By.XPATH, check_one))
                time.sleep(2)

                check_type.select_by_visible_text(df_new['Check Type'][a])
                doc_one = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[3]/div/div/div/div/select".format(a-4)
                doc_type = Select(driver.find_element(By.XPATH, doc_one))
                time.sleep(4)

                doc_type.select_by_visible_text(df_new['Document Type'][a])
                browse_click = driver.find_element(By.XPATH, "//*[@id='abc']/fieldset/span")
            else:
                name_one = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[1]/div/div/div/div/select".format(a+1)
                map_name = Select(driver.find_element(By.XPATH, name_one))
                time.sleep(7)
                map_name.select_by_visible_text(file_name)
                
                check_one = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[2]/div/div/div/div/select".format(a+1)
                check_type = Select(driver.find_element(By.XPATH, check_one))
                time.sleep(2)
                check_type.select_by_visible_text(df_new['Check Type'][a])
                
                doc_one = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[11]/div/div/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[3]/div/div/div/div/select".format(a+1)
                doc_type = Select(driver.find_element(By.XPATH, doc_one))
                time.sleep(4)
                doc_type.select_by_visible_text(df_new['Document Type'][a])

                browse_click = driver.find_element(By.XPATH, "//*[@id='abc']/fieldset/span")

        next_pagep=driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[13]/div[2]/div/div/div[4]/div/div/div/button")
        next_pagep.click()
        
    #     ## calling Test list
    #     if len(error) == 0:
    #         pass
    #     else:
    #         raise Exception('Mandatory Field is Empty but still the Flow Proceed')
            
        if pd.isna(check_edu):
            print('not educational check')
        else:
            print('Its an educational check')
            educational_check_ia()
        if pd.isna(check_emp):
            print('not employment check')
        else:
            print('Its an employment check')
            employment_check_ia()
        if pd.isna(check_licen):
            print('not license check')
        else:
            print('Its a license check')
            health_check_ia()
        if pd.isna(check_good):
            print('not good standing check')
        else:
            print('Its a good standing check')
            good_standing_ia()
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='combo_div_2']")))

        pay_sub_mode = driver.find_element(By.XPATH, "//*[@id='combo_div_2']")
        pay_sub_mode.send_keys("Invoice")
        time.sleep(1)
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[2]/div/div/div[5]/div/div/div/button")))

        submit_case_submission = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[2]/div/div/div[5]/div/div/div/button")
        submit_case_submission.click()
        time.sleep(6)


    # Create a button to start the dynamic updating process
    start_button = st.button("Start Running Cases")

    # Define an empty pie chart variable
    pie_chart = None

    # Define an empty bar chart variable
    bar_chart = None

    # Create a placeholder for the pie chart and bar chart
    col1, col2 = st.columns(2)
    pie_chart_placeholder = col1.empty()
    bar_chart_placeholder = col2.empty()

    if start_button:
        for i in range(0, len(df)):
            # Generate sample data for pie charts
            pie_data = {'category': ['Cases Pending', 'Cases Completed'], 'value': [len(df), i]}

            # Generate sample data for bar charts
            bar_data = {'category': ['Total Cases', 'Cases Passed', 'Cases Failed'], 'value': [len(df_moe), i, i]}

            # Update the data of the pie chart
            pie_chart = create_pie_chart(pie_data)

            # Update the data of the bar chart
            bar_chart = create_bar_chart(bar_data)

            # Display the updated pie chart and bar chart in their respective placeholders
            pie_chart_placeholder.plotly_chart(pie_chart, use_container_width=True)
            bar_chart_placeholder.plotly_chart(bar_chart, use_container_width=True)

            # Add a delay to simulate real-time updates
            time.sleep(1)



#### Resource Page
def Resources():
    st.title("Resouces Required")
    st.write("download the required csv files")
    df = pd.read_csv("Validation Data(FQC) - Validation Data(FQC).csv")
    csv_data = df.to_csv(index=False).encode('utf-8-sig') 

    df_veri = pd.read_csv("Documents Mapping  - Sheet1.csv")
    csv_data_veri = df.to_csv(index=False).encode('utf-8-sig') 
    
    # Create a download button
    btn_1 = st.download_button(
        label="Download Validation DATA(FQC)",
        data=csv_data,
        file_name="validation.csv",
        mime="text/csv"
    )

    btn_2 = st.download_button(
        label="Download Document Mapping",
        data=csv_data,
        file_name="mapping.csv",
        mime="text/csv"
    )

#### Result Page
def Result():
    st.title("Download Result")
    st.write("download the result of cases run")

def main():
    st.sidebar.title("Navigation")
    pages = {
        "Home": app,
        "Resources": Resources,
        "Result": Result
    }
    
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    pages[selected_page]()

if __name__ == "__main__":
    main()