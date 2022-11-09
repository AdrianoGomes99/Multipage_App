import dash
import psycopg2 as pg
from pycaret.classification import predict_model, load_model
import pandas as pd
import numpy as np
import pathlib    


# meta_tags are required for the app layout to be mobile responsive
APP = dash.Dash(__name__, suppress_callback_exceptions=True,
                assets_external_path='https://cdn.tailwindcss.com',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
SERVER = APP.server

   
con = pg.connect(host = "localhost",
    port = 5432,
    database="Augmanity_A29",
    user="postgres",
    password="postgres"
)
#cursor = con.cursor()

query = 'SELECT ic."IdInternalCollaborator", co."IdContract", ic."Gender", icms."IdMaritalStatus", icql."IdQualificationLevel", icsa."IdStudyArea", ics."Nationality", EXTRACT(year FROM age(now(), ic."Birthday"::timestamp without time zone::timestamp with time zone)) AS age, ics."Duration", ics."NumDependents", ics."NumHolders", ics."NumDisabledDependents", co."IdArea", co."IdCategoryProfessional", co."IdTypeContract", co."IdSchedule", co."IdDayOff", CASE WHEN co."EntryDate" < now() AND co."LeaveDate" IS NOT NULL AND co."LeaveDate" < now() THEN round(EXTRACT(year FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) + EXTRACT(month FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) / 12::numeric + EXTRACT(day FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) / 365.25, 1)  ELSE round(EXTRACT(year FROM age(now(), co."EntryDate"::timestamp with time zone)) + EXTRACT(month FROM age(now(), co."EntryDate"::timestamp with time zone)) / 12::numeric + EXTRACT(day FROM age(now(), co."EntryDate"::timestamp with time zone)) / 365.25, 1)  END AS yearsatcompany, co."SalaryRate", co."MorningSchedule", co."AfternoonSchedule", co."NightSchedule", co."WeekendSchedule"  FROM "Contract" co, "Area" ar, "InternalCollaborator" ic, "InternalCollaborator_MaritalStatus" icms, "InternalCollaborator_QualificationLevel" icql, "InternalCollaborator_StudyArea" icsa, "InternalCollaborator_Status" ics WHERE co."IdArea" = ar."IdArea" AND co."IdInternalCollaborator" = ic."IdInternalCollaborator" AND co."LeaveDate" IS NULL AND ic."IdInternalCollaborator" = ics."IdInternalCollaborator" AND ic."IdInternalCollaborator" = icql."IdInternalCollaborator" AND ic."IdInternalCollaborator" = icsa."IdInternalCollaborator" AND ic."IdInternalCollaborator" = icms."IdInternalCollaborator";'
#

RAW_DATA = pd.read_sql(query, con)

# get relative data folder
PATH = pathlib.Path(__file__).parent
MODEL_PATH = PATH.joinpath("../Multipage_App/static").resolve()
# ML model for attrition prediction (xgboost in joblib format)
MODEL = load_model(MODEL_PATH.joinpath("tuned_xgboost_pycaret"))


#%%

# Functions to clean data
def gender_sex(g):
    if g=='M':
        return 'Male'
    elif g=='F':
        return 'Female'
    else:
        #melhorar sistema de erros
        raise ValueError ('gender_sex')
    
def idMaritalStatus_MaritalStatus(mar):
    if mar==1:
        return 'Single'
    elif mar==2:
        return 'NMP'
    elif mar==3:
        return 'Married'
    elif mar==4:
        return 'Divorced'
    elif mar==5:
        return 'Widowed'
    else:
        #melhorar sistema de erros
        raise ValueError ('idMaritalStatus_MaritalStatus')

def idQualificationLevel_Academic_Qualifications (aq):
    if aq == 1:
        return '1' #2nd cycle of basic education
    elif aq == 2:
        return '2' #3rd cycle of basic education, obtained in regular education or through courses of dual certification
    elif aq == 3:
        return '3' #Secondary education aimed at pursuing higher level studies
    elif aq == 4:
        return '4' #Secondary education obtained through dual certification pathways or secondary education aimed at pursuing higher level studies plus a professional internship
    elif aq == 5:
        return '5' #Non-higher post-secondary level qualification with credits for pursuing higher level studies
    elif aq == 6:
        return '6' #Degree
    elif aq == 7:
        return '7' #Masters
    elif aq == 8:
        return '8' #Doctorate
    else:
        #melhorar sistema de erros
        raise ValueError ('idQualificationLevel_Academic_Qualifications')
    
def idStudyArea_Study_Area (s):
    if s == 1:
        return 'Teacher_EducationalSciences'
    elif s == 2:
        return 'Arts'
    elif s == 3:
        return 'Humanities'
    elif s == 4:
        return 'Social_BehavioralSciences'
    elif s == 5:
        return 'Information_Journalism'
    elif s == 6:
        return 'Business_Sciences'
    elif s == 7:
        return 'Law' 
    elif s == 8:
        return 'Life_Sciences'
    elif s == 9:
        return 'Physical_Sciences'
    elif s == 10:
        return 'Mathematics_Statistics'
    elif s == 11:
        return 'Informatics'
    elif s == 12:
        return 'Engineering'
    elif s == 13:
        return 'Unknown' #'Manufacturing_Industries' not in model
    elif s == 14:
        return 'Architecture_Construction'
    elif s == 15:
        return 'Agriculture_Forestry_Fisheries'
    elif s == 16:
        return 'Veterinary_Sciences'
    elif s == 17:
        return 'Health'
    elif s == 18:
        return 'Social_Services'
    elif s == 19:
        return 'Personal_Services'
    elif s == 20:
        return 'Unknown' #'Transport_Services' not in model
    elif s == 21:
        return 'Environmental_Protection'
    elif s == 22:
        return 'Security_Services'
    elif s == 23:
        return 'Unknown'
    elif s == 24:
        return 'Without_Area'
    elif s == 25:
        return 'Professional_Course'
    else:
        #melhorar sistema de erros
        raise ValueError ('idStudyArea_Study_Area')

def idArea_Area (a):
    if a == 1:
        return 'Administration/Management'
    elif a == 2:
        return 'Financial'
    elif a == 3:
        return 'IT' 
    elif a == 4:
        return 'HR'
    elif a == 5:
        return 'Logistics' 
    elif a == 6:
        return 'Commercial/Marketing' 
    elif a == 7:
        return 'Engineering_Research' 
    elif a == 8:
        return 'Production' 
    elif a == 9:
        return 'Quality'
    elif a == 10:
        return 'Maintenance'
    else:
        #melhorar sistema de erros
        raise ValueError ('idArea_Area')
        
def idCategoryProfessional_Qualifications (q):
    if q == 1:
        return 'Superior_Managers'
    elif q == 2:
        return 'Middle_Managers'
    elif q == 3:
        return 'Managers_Foremen_Masters_TeamLeaders'
    elif q == 4:
        return 'Highly_Qualified_Professional'
    elif q == 5:
        return 'Qualified_Professional'
    elif q == 6:
        return 'SemiQualified_Professional'
    elif q == 7:
        return 'Unqualified_Professional'
    elif q == 8:
        return 'Practitioner_Apprentice'
    elif q == 9:
        return 'Practitioner_Apprentice' #'Apprentice' not in model
    else:
        #melhorar sistema de erros
        raise ValueError ('idCategoryProfessional_Qualifications')
    
def idTypeContract_Contract_Type (ct):
    if ct == 1 :
        return 'Fixed_Term'
    elif ct == 2 :
        return 'Uncertain_Term'
    elif ct == 3 :
        return 'No_Term'
    else:
        #melhorar sistema de erros
        raise ValueError ('idTypeContract_Contract_Type')
    
def idSchedule_Schedule (sch):
    if sch == 1 :
        return 'Fixed'
    elif sch == 2 :
        return 'Concentrated'
    elif sch == 3 :
        return 'Rotating'
    else:
        #melhorar sistema de erros
        raise ValueError ('idSchedule_Schedule')
        
def idDayOff_Day_off (do):
    if do == 1:
        return 'Fixed_Week'
    elif do == 2:
        return 'Fixed_Weekend'
    elif do == 3 :
        return 'Rotating'
    else:
        #melhorar sistema de erros
        raise ValueError ('idDayOff_Day_off')
        
def morningSchedule_Morning_Schedule (msch):
    if msch == True:
        return 'Yes'
    elif msch == False:
        return 'No'
    else:
        #melhorar sistema de erros
        raise ValueError ('morningSchedule_Morning_Schedule')
        
def afternoonSchedule_Afternoon_Schedule (asch):
    if asch == True:
        return 'Yes'
    elif asch == False:
        return 'No'
    else:
        #melhorar sistema de erros
        raise ValueError ('afternoonSchedule_Afternoon_Schedule')
        
def nightSchedule_Night_Schedule (nsch):
    if nsch == True:
        return 'Yes'
    elif nsch == False:
        return 'No'
    else:
        #melhorar sistema de erros
        raise ValueError ('nightSchedule_Night_Schedule')
        
def weekendSchedule_Weekend_Schedule (wsch):
    if wsch == True:
        return 'Yes'
    elif wsch == False:
        return 'No'
    else:
        #melhorar sistema de erros
        raise ValueError ('weekendSchedule_Weekend_Schedule')
        
## create a pandas df for the model
def transform_df(df_json):
    df_model = pd.DataFrame()
    df_model['idInternalCollaborator']=df_json['IdInternalCollaborator']
    df_model['idContract']=df_json['IdContract']
    df_model['Sex']=df_json['Gender'].apply(gender_sex)
    df_model['Marital_Status']=df_json['IdMaritalStatus'].apply(idMaritalStatus_MaritalStatus)
    df_model['Academic_Qualifications']=df_json['IdQualificationLevel'].apply(idQualificationLevel_Academic_Qualifications)
    df_model['Study_Area']=df_json['IdStudyArea'].apply(idStudyArea_Study_Area)
    df_model['Nationality']=df_json['Nationality'] 
    df_model['Age']=df_json['age'] 
    df_model['Duration']=df_json['Duration'] 
    df_model['Number_Dependents']=df_json['NumDependents'] 
    df_model['Number_holders']=df_json['NumHolders'] 
    df_model['Number_Disabled_Dependents']=df_json['NumDisabledDependents'] 
    df_model['Area']=df_json['IdArea'].apply(idArea_Area)
    df_model['Qualifications']=df_json['IdCategoryProfessional'].apply(idCategoryProfessional_Qualifications)
    df_model['Contract_Type']=df_json['IdTypeContract'].apply(idTypeContract_Contract_Type)
    df_model['Schedule']=df_json['IdSchedule'].apply(idSchedule_Schedule)
    df_model['Day_off']=df_json['IdDayOff'].apply(idDayOff_Day_off)
    df_model['Float_Year_at_Company']=df_json['yearsatcompany'] 
    df_model['Salary_Rate']=df_json['SalaryRate']
    df_model['Morning_Schedule']=df_json['MorningSchedule'].apply(morningSchedule_Morning_Schedule)
    df_model['Afternoon_Schedule']=df_json['AfternoonSchedule'].apply(afternoonSchedule_Afternoon_Schedule)
    df_model['Night_Schedule']=df_json['NightSchedule'].apply(nightSchedule_Night_Schedule)
    df_model['Weekend_Schedule']=df_json['WeekendSchedule'].apply(weekendSchedule_Weekend_Schedule)
    return df_model

#%%

# def create_df(json_str):
    
#     json_dict = json.loads(json_str)  
#     df_json = pd.DataFrame.from_records(json_dict)    
#     df_model = transform_df(df_json)
    
#     df_pred = predict_model(estimator = MODEL, data= df_model)
#     df_pred['Attrition'] = df_pred['Label']
#     df_pred['Attrition'] = np.where(df_pred['Label']=='Employee', 'Voluntary', df_pred['Attrition'])
#     df_pred['Attrition'] = np.where(df_pred['Label']=='Company', 'Involuntary', df_pred['Attrition'])
#     df_pred['Attrition'] = np.where(df_pred['Label']=='No', 'No', df_pred['Attrition'])
    
#     df_results = predict_model(estimator = MODEL, data= df_model, raw_score = True)
#     df_results['Attrition'] = df_pred['Attrition']
#     df_results.rename(columns = {'Score_No':'ValueStay', 
#                                  'Score_Employee':'ValueVoluntary', 
#                                  'Score_Company':'ValueInvoluntary'},
#                       inplace=True)
    
#     date_today = pd.to_datetime("today").strftime("%d-%m-%Y")
#     df_results['DateComputed'] = date_today

#     return df_results


# json_str = r'''[{"idInternalCollaborator":127,"idContract":106,"gender":"F","idMaritalStatus":3,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":48,"duration":756.5,"numDependents":0,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":31.3,"salaryRate":-3.284980535507202,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":143,"idContract":122,"gender":"F","idMaritalStatus":3,"idQualificationLevel":7,"idStudyArea":4,"nationality":"PT","age":46,"duration":775.2999877929688,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":22.8,"salaryRate":-10.66496467590332,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":398,"idContract":377,"gender":"F","idMaritalStatus":3,"idQualificationLevel":3,"idStudyArea":24,"nationality":"PT","age":44,"duration":623.0,"numDependents":0,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":25.4,"salaryRate":-14.7932767868042,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":487,"idContract":466,"gender":"F","idMaritalStatus":3,"idQualificationLevel":3,"idStudyArea":24,"nationality":"PT","age":42,"duration":1105.0999755859375,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":23.2,"salaryRate":-12.817984580993652,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":667,"idContract":646,"gender":"M","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":12,"nationality":"PT","age":39,"duration":1645.800048828125,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":10.4,"salaryRate":14.077670097351074,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":671,"idContract":650,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":10,"nationality":"PT","age":35,"duration":952.7000122070312,"numDependents":1,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":10.0,"salaryRate":-8.770228385925293,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":673,"idContract":652,"gender":"M","idMaritalStatus":3,"idQualificationLevel":7,"idStudyArea":12,"nationality":"PT","age":37,"duration":1613.4000244140625,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":9.5,"salaryRate":12.003530502319336,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":677,"idContract":656,"gender":"F","idMaritalStatus":5,"idQualificationLevel":3,"idStudyArea":24,"nationality":"PT","age":50,"duration":589.4000244140625,"numDependents":2,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":31.9,"salaryRate":12.784847259521484,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":681,"idContract":660,"gender":"F","idMaritalStatus":4,"idQualificationLevel":6,"idStudyArea":6,"nationality":"PT","age":43,"duration":1015.7000122070312,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":23.4,"salaryRate":20.610240936279297,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":682,"idContract":661,"gender":"F","idMaritalStatus":3,"idQualificationLevel":4,"idStudyArea":24,"nationality":"PT","age":42,"duration":608.4000244140625,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":21.3,"salaryRate":-14.93471622467041,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":684,"idContract":663,"gender":"F","idMaritalStatus":3,"idQualificationLevel":7,"idStudyArea":10,"nationality":"PT","age":42,"duration":2752.10009765625,"numDependents":1,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":12.6,"salaryRate":-3.614457845687866,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":697,"idContract":676,"gender":"M","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":10,"nationality":"CH","age":62,"duration":3180.39990234375,"numDependents":4,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":24.4,"salaryRate":8.856575012207031,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":701,"idContract":680,"gender":"F","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":6,"nationality":"PT","age":48,"duration":191.3000030517578,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":25.0,"salaryRate":-13.650349617004395,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":704,"idContract":683,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":4,"nationality":"PT","age":43,"duration":615.0,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":14.1,"salaryRate":-17.581642150878906,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":769,"idContract":748,"gender":"M","idMaritalStatus":3,"idQualificationLevel":3,"idStudyArea":24,"nationality":"PT","age":54,"duration":574.4000244140625,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":33.9,"salaryRate":37.72554016113281,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":774,"idContract":753,"gender":"M","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":12,"nationality":"PT","age":47,"duration":2051.10009765625,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":14.2,"salaryRate":1.3662842512130737,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":806,"idContract":785,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":32,"duration":601.7999877929688,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":7.9,"salaryRate":-11.738746643066406,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":853,"idContract":832,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":4,"nationality":"PT","age":33,"duration":3280.5,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":7.0,"salaryRate":2.4096386432647705,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":858,"idContract":837,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":34,"duration":495.8999938964844,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":6.9,"salaryRate":2.4096386432647705,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":967,"idContract":946,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":28,"duration":2766.199951171875,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":5.0,"salaryRate":-12.650602340698242,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":995,"idContract":974,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":34,"duration":855.0999755859375,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":4.5,"salaryRate":-10.238266944885254,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":1051,"idContract":1030,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":30,"duration":5189.10009765625,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":3.3,"salaryRate":-13.94527816772461,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":1184,"idContract":1163,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":12,"nationality":"PT","age":27,"duration":2425.89990234375,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":1.2,"salaryRate":-27.260089874267578,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":1204,"idContract":1183,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":6,"nationality":"PT","age":24,"duration":1097.699951171875,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":1.0,"salaryRate":-9.514381408691406,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},
# {"idInternalCollaborator":72,"idContract":51,"gender":"M","idMaritalStatus":3,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":33,"duration":738.4000244140625,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":3.3,"salaryRate":-20.471031188964844,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":94,"idContract":73,"gender":"F","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":12,"nationality":"PT","age":36,"duration":675.0999755859375,"numDependents":0,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":3.7,"salaryRate":-22.410762786865234,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":118,"idContract":97,"gender":"M","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":6,"nationality":"PT","age":54,"duration":809.7999877929688,"numDependents":0,"numHolders":2,"numDisabledDependents":0,"idArea":2,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":30.3,"salaryRate":7.221114158630371,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},
# {"idInternalCollaborator":128,"idContract":107,"gender":"F","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":4,"nationality":"PT","age":40,"duration":580.5,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":14.6,"salaryRate":-6.423308849334717,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":129,"idContract":108,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":3,"nationality":"PT","age":41,"duration":940.5,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":13.8,"salaryRate":-15.500882148742676,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":679,"idContract":658,"gender":"F","idMaritalStatus":3,"idQualificationLevel":4,"idStudyArea":24,"nationality":"PT","age":50,"duration":632.7999877929688,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":30.6,"salaryRate":21.21525764465332,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":680,"idContract":659,"gender":"F","idMaritalStatus":3,"idQualificationLevel":4,"idStudyArea":24,"nationality":"PT","age":51,"duration":794.7999877929688,"numDependents":3,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":29.4,"salaryRate":25.308103561401367,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":683,"idContract":662,"gender":"F","idMaritalStatus":3,"idQualificationLevel":3,"idStudyArea":24,"nationality":"PT","age":39,"duration":370.6000061035156,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":19.3,"salaryRate":-3.330232620239258,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":722,"idContract":701,"gender":"M","idMaritalStatus":4,"idQualificationLevel":6,"idStudyArea":17,"nationality":"PT","age":65,"duration":1027.300048828125,"numDependents":2,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":30.6,"salaryRate":0.04898499697446823,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":838,"idContract":817,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":31,"duration":823.2999877929688,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":6.6,"salaryRate":3.706972599029541,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":855,"idContract":834,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":4,"nationality":"PT","age":32,"duration":3063.5,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":7.0,"salaryRate":28.406707763671875,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":874,"idContract":853,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":6,"nationality":"PT","age":31,"duration":1181.0999755859375,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":6.6,"salaryRate":-3.614457845687866,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":1043,"idContract":1022,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":4,"nationality":"PT","age":30,"duration":3093.0,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":3.4,"salaryRate":-1.4563106298446655,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":1124,"idContract":1103,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":3,"nationality":"PT","age":31,"duration":9438.2998046875,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":1.5,"salaryRate":-11.738746643066406,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":1194,"idContract":1173,"gender":"F","idMaritalStatus":1,"idQualificationLevel":7,"idStudyArea":3,"nationality":"PT","age":26,"duration":4115.39990234375,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":1.1,"salaryRate":-10.84337329864502,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},
# {"idInternalCollaborator":81,"idContract":60,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":4,"nationality":"PT","age":27,"duration":1208.0,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":2.4,"salaryRate":-20.372655868530273,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":85,"idContract":64,"gender":"F","idMaritalStatus":1,"idQualificationLevel":6,"idStudyArea":6,"nationality":"PT","age":24,"duration":2775.0,"numDependents":0,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":1,"idSchedule":1,"idDayOff":2,"yearsatcompany":1.5,"salaryRate":-13.133806228637695,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":97,"idContract":76,"gender":"M","idMaritalStatus":5,"idQualificationLevel":6,"idStudyArea":6,"nationality":"PT","age":61,"duration":1096.0999755859375,"numDependents":1,"numHolders":1,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":42.3,"salaryRate":8.86201286315918,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":109,"idContract":88,"gender":"F","idMaritalStatus":3,"idQualificationLevel":3,"idStudyArea":24,"nationality":"PT","age":59,"duration":497.3999938964844,"numDependents":1,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":5,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":32.3,"salaryRate":7.978723526000977,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false},{"idInternalCollaborator":119,"idContract":98,"gender":"F","idMaritalStatus":3,"idQualificationLevel":6,"idStudyArea":4,"nationality":"PT","age":41,"duration":1524.5999755859375,"numDependents":2,"numHolders":2,"numDisabledDependents":0,"idArea":4,"idCategoryProfessional":1,"idTypeContract":3,"idSchedule":1,"idDayOff":2,"yearsatcompany":12.5,"salaryRate":14.606912612915039,"morningSchedule":true,"afternoonSchedule":false,"nightSchedule":false,"weekendSchedule":false}
# ]''' 


# DATA = create_df(json_str)

#%%
def create_df(df):
    df_model = transform_df(df)
    
    df_pred = predict_model(estimator = MODEL, data= df_model)
    df_pred['Attrition'] = df_pred['Label']
    df_pred['Attrition'] = np.where(df_pred['Label']=='Employee', 'Voluntary', df_pred['Attrition'])
    df_pred['Attrition'] = np.where(df_pred['Label']=='Company', 'Involuntary', df_pred['Attrition'])
    df_pred['Attrition'] = np.where(df_pred['Label']=='No', 'No', df_pred['Attrition'])
    
    df_results = predict_model(estimator = MODEL, data= df_model, raw_score = True)
    df_results['Attrition'] = df_pred['Attrition']
    df_results.rename(columns = {'Score_No':'ValueStay', 
                                 'Score_Employee':'ValueVoluntary', 
                                 'Score_Company':'ValueInvoluntary'},
                      inplace=True)
    
    date_today = pd.to_datetime("today").strftime("%d-%m-%Y")
    df_results['DateComputed'] = date_today

    return df_results


DATA = create_df(RAW_DATA)

#area with highest voluntary attrition proportion
DEFAULT_AREA = str(pd.DataFrame(pd.crosstab(DATA.Area,DATA.Attrition, normalize='index')).loc[:,'Voluntary'].idxmax())

#%%

#Save results to database
BD_DATA = DATA.loc[:,['idContract','DateComputed', 'ValueStay', 'ValueVoluntary', 'ValueInvoluntary']] # limitar as colunas
#BD_DATA.to_sql(name='Attrition', con=con, if_exists='append', index=False)
BD_DATA.rename(columns = {'idContract':'IdContract'}, inplace=True)

def execute_mogrify(conn, df, table):
    """
    Using cursor.mogrify() to build the bulk insert query
    then cursor.execute() to execute the query
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    ##### cols = ','.join(list(df.columns))
    # SQL quert to execute
    cursor = conn.cursor()
    values = [cursor.mogrify('(%s,%s,%s,%s,%s)', tup).decode('utf8') for tup in tuples]
    query  = 'INSERT INTO "%s" ("IdContract", "DateComputed", "ValueStay", "ValueVoluntary", "ValueInvoluntary") VALUES ' % (table) + ','.join(values)
    
    try:
        cursor.execute(query, tuples)
        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_mogrify() done")
    cursor.close()

execute_mogrify(con, BD_DATA, 'Attrition')

#%%



# functions to get the list/dict of existing areas in the dataframe
# this dictionary will be usefull for the dropdown in the dashboards
def get_areas_dict(df):
    areas = df.Area.unique().tolist()
    areas_dict = {'Administration/Management' : 'Administration & Management',
                    'HR' : 'Human Resources',
                    'Financial' : 'Financial', 
                    'IT' : 'Information Technology',
                    'Engineering_Research' : 'Engineering & Research',
                    'Production' : 'Production',
                    'Commercial/Marketing' : 'Commercial & Marketing',
                    'Logistics' : 'Logistics',
                    'Quality' : 'Quality',
                    'Maintenance' : 'Maintenance' }
    
    options_dict = {k:areas_dict[k] for k in areas_dict.keys() if k in areas}

    return options_dict

AREAS = get_areas_dict(DATA)

### LST_IDS = [] #DATA.idContract.unique().tolist()

LST_DEFAULT_AREA = []

DEFAULT_ATT = 'Voluntary'