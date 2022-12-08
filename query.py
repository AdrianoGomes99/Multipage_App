# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:12:33 2022

@author: aog
"""

query = '

SELECT 
            ic."IdInternalCollaborator", 
            co."IdContract", 
            ic."Gender", 
            icms."IdMaritalStatus", 
            icql."IdQualificationLevel", 
            icsa."IdStudyArea", 
            ics."Nationality", 
            #age is calculated as the diference between now and birthday
            EXTRACT(year FROM age(now(), ic."Birthday"::timestamp without time zone::timestamp with time zone)) AS age, 
            ics."Duration", 
            ics."NumDependents", 
            ics."NumHolders", 
            ics."NumDisabledDependents", 
            co."IdArea", 
            co."IdCategoryProfessional", 
            co."IdTypeContract", 
            co."IdSchedule", 
            co."IdDayOff", 
    
    CASE WHEN 
            #entry date should be before now
            co."EntryDate" < now() 
            # if Leave date exists and is before now
            AND co."LeaveDate" IS NOT NULL 
            AND co."LeaveDate" < now() 
        THEN round(
            #years at company are calculated as diference between leave date and entry date
            EXTRACT(year FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) 
            + EXTRACT(month FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) / 12::numeric 
            + EXTRACT(day FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) / 365.25, 1)  
            #if not (there is no leave date)
        ELSE round(
            #years at company are calculated as diference between now date and entry date
            EXTRACT(year FROM age(now(), co."EntryDate"::timestamp with time zone)) 
            + EXTRACT(month FROM age(now(), co."EntryDate"::timestamp with time zone)) / 12::numeric 
            + EXTRACT(day FROM age(now(), co."EntryDate"::timestamp with time zone)) / 365.25, 1)  
        END AS yearsatcompany, 
    
    co."SalaryRate", 
    co."MorningSchedule", 
    co."AfternoonSchedule", 
    co."NightSchedule", 
    co."WeekendSchedule"  
    
    FROM 
    "Contract" co, 
    "Area" ar, 
    "InternalCollaborator" ic, 
    "InternalCollaborator_MaritalStatus" icms, 
    "InternalCollaborator_QualificationLevel" icql, 
    "InternalCollaborator_StudyArea" icsa, 
    "InternalCollaborator_Status" ics 
    
    WHERE co."IdArea" = ar."IdArea" 
    AND co."IdInternalCollaborator" = ic."IdInternalCollaborator" 
    #only for active employees
    AND co."LeaveDate" IS NULL 
    AND ic."IdInternalCollaborator" = ics."IdInternalCollaborator" 
    AND ic."IdInternalCollaborator" = icql."IdInternalCollaborator" 
    AND ic."IdInternalCollaborator" = icsa."IdInternalCollaborator" 
    AND ic."IdInternalCollaborator" = icms."IdInternalCollaborator";'
