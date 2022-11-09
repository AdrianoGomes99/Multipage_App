import pandas as pd
import psycopg2 as pg
   
con = pg.connect(host = "localhost",
    port = 5432,
    database="Augmanity_A30",
    user="postgres",
    password="postgres"
)
cursor = con.cursor()

query = 'SELECT ic."IdInternalCollaborator", co."IdContract", ic."Gender", icms."IdMaritalStatus", icql."IdQualificationLevel", icsa."IdStudyArea", ics."Nationality", EXTRACT(year FROM age(now(), ic."Birthday"::timestamp without time zone::timestamp with time zone)) AS age, ics."Duration", ics."NumDependents", ics."NumHolders", ics."NumDisabledDependents", co."IdArea", co."IdCategoryProfessional", co."IdTypeContract", co."IdSchedule", co."IdDayOff", CASE WHEN co."EntryDate" < now() AND co."LeaveDate" IS NOT NULL AND co."LeaveDate" < now() THEN round(EXTRACT(year FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) + EXTRACT(month FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) / 12::numeric + EXTRACT(day FROM age(co."LeaveDate"::timestamp with time zone, co."EntryDate"::timestamp with time zone)) / 365.25, 1)  ELSE round(EXTRACT(year FROM age(now(), co."EntryDate"::timestamp with time zone)) + EXTRACT(month FROM age(now(), co."EntryDate"::timestamp with time zone)) / 12::numeric + EXTRACT(day FROM age(now(), co."EntryDate"::timestamp with time zone)) / 365.25, 1)  END AS yearsatcompany, co."SalaryRate", co."MorningSchedule", co."AfternoonSchedule", co."NightSchedule", co."WeekendSchedule"  FROM "Contract" co, "Area" ar, "InternalCollaborator" ic, "InternalCollaborator_MaritalStatus" icms, "InternalCollaborator_QualificationLevel" icql, "InternalCollaborator_StudyArea" icsa, "InternalCollaborator_Status" ics WHERE co."IdArea" = ar."IdArea" AND co."IdInternalCollaborator" = ic."IdInternalCollaborator" AND co."LeaveDate" IS NULL AND ic."IdInternalCollaborator" = ics."IdInternalCollaborator" AND ic."IdInternalCollaborator" = icql."IdInternalCollaborator" AND ic."IdInternalCollaborator" = icsa."IdInternalCollaborator" AND ic."IdInternalCollaborator" = icms."IdInternalCollaborator";'
  
data = pd.read_sql(query, con)
#print(data)

#tables = data["table_name"].unique()
#print("List of tables: ", tables)

print(data)

print(data.columns)