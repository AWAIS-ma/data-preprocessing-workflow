import pandas as p
import matplotlib.pyplot as mt
data = p.read_excel("dummy_dataset.xlsx") 

new_data = []

for i, val in data.iterrows():
    for j in range(1, 4):
        rolno = val.get(f'Roll No.{j}')
        name = val.get(f'Name {j}')
        if p.notna(rolno) and p.notna(name):
            new_data.append({
                'Project ID': val['Project ID'],
                'Project Title': val['Project Title'],
                'Student Roll No': int(rolno),
                'Student Name': name,
                'Supervisor': val['Supervisor']
            })

reshaped_new_data = p.DataFrame(new_data)
print("\tReshaped Data:\n")
print(reshaped_new_data.to_string(index=False))
# .head(10).to_string(index=False)

print("\n\tDuplicate Roll Numbers Across Projects:\n")
all_duplicates = reshaped_new_data.duplicated(subset='Student Roll No', keep=False)
if all_duplicates.any():
    print("\tDuplicates roll numbers are : \n")
    print(reshaped_new_data[all_duplicates].to_string(index=False))
else:
    print(" No duplicate roll numbers are present")

print("\n\tAll Missing Values :\n")
print(reshaped_new_data.isnull().sum().to_string())
print("\n\tProjects Supervised by Each Supervisor:\n")
supervisor_projects = reshaped_new_data[['Project ID', 'Supervisor']].drop_duplicates()
project_counts = supervisor_projects['Supervisor'].value_counts()
print(project_counts.to_string())
print("\n\tPivot Table:\n")
pivot_table = p.pivot_table(
    reshaped_new_data,
    index='Supervisor',
    columns='Project Title',
    values='Student Roll No',
    aggfunc='count',
    fill_value=0
)
print(pivot_table)

mt.figure(figsize=(8, 4))
project_counts.plot(kind='bar', color='black', edgecolor='black')
mt.title('Number of Projects Supervised by Each Supervisor')
mt.xlabel('Supervisor')
mt.ylabel('Number of Projects')
mt.xticks(rotation=30, ha='right')
mt.tight_layout()
mt.show()

# reshaped_new_data.to_excel("Reshaped_data.xlsx")
pivot_table.to_csv("pivot_table_summary.csv")