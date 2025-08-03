# Day 1 Conext Scenario:  WhatsApp Group Size Engagement Analysis 
# You are a Product Analyst on the WhatsApp team investigating group messaging dynamics. Your team wants to 
# understand how large groups are being used and their messaging patterns. You'll leverage data to uncover 
# insights about group participation and communication behaviors.
# What is the maximum number of participants among WhatsApp groups that were created in October 2024? 
# This metric will help us understand the largest group size available.
#
# # Assumptions: Pandas is imported as pd and NumPy is imported as np. 
# DataFrames with the same names: dim_groups.  
# The final answer needs to be printed as a data frame or final results.  
# Tables included: dim_groups(group_id, created_date, participant_count, total_messages)
#
# Find the maximum participant count among WhatsApp groups created in October 2024 using the dim_groups DataFrame.
#
# Strategy: 
# - Filter dim_groups for rows where created_date falls within October 2024. 
# - Extract the maximum value from the participant)count column of that filtered subset. 
# - Wrap it up neatly as a DataFrame for clean presentation. 
#
# Step 1: Convert 'created_date' to datetime if it's not already
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# Step 2: Filter for groups created in October 2024
october_2024_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10)
]

# Step 3: Find the maximum participant count
max_participants = october_2024_groups['participant_count'].max()

# Step 4: Present results as a DataFrame
result_df = pd.DataFrame({
    'Max Participants in Oct 2024 Groups': [max_participants]
})

# Step 5: Display the result
print(result_df)

# Question 2: What is the average number of participants in WhatsApp groups that were created in October 2024? 
# This number will indicate the typical group size and inform our group messaging feature considerations.
#
# Approach: 
# - Ensure datetime consistency by converting created_date. 
# - Filter for October 2024 groups.
# - Calculate the mean of the participant_count column. 
# - Wrap it up in a Dataframe to keep outputs clean for use or preentations. 
# 
# Step 1: Convert 'created_date' to datetime if needed
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# Step 2: Filter for groups created in October 2024
october_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10)
]

# Step 3: Calculate average participant count
average_participants = october_groups['participant_count'].mean()

# Step 4: Present the result as a DataFrame
result_df = pd.DataFrame({
    'Average Participants in Oct 2024 Groups': [average_participants]
})

# Step 5: Display the result
print(result_df)

# For WhatsApp groups with more than 50 participants that were created in October 2024, what is the average number
# of messages sent? This insight will help assess engagement in larger groups and support recommendations for 
# group messaging features.
#
# Approach:
# - Convert created_date to datetime if needed.
# - Filter dim_groups for October 2024.
# - Further filter for groups where participant_count > 50.
# - Calculate the mean of the total_messages column.
# - Return it as a DataFrame for consistency.

# Step 1: Ensure datetime format
dim_groups['created_date'] = pd.to_datetime(dim_groups['created_date'])

# Step 2: Filter for October 2024 groups
october_groups = dim_groups[
    (dim_groups['created_date'].dt.year == 2024) &
    (dim_groups['created_date'].dt.month == 10)
]

# Step 3: Filter for groups with more than 50 participants
large_october_groups = october_groups[october_groups['participant_count'] > 50]

# Step 4: Calculate average number of messages
average_messages = large_october_groups['total_messages'].mean()

# Step 5: Present result
result_df = pd.DataFrame({
    'Avg Messages in Oct 2024 Large Groups (>50 participants)': [average_messages]
})

# Step 6: Display
print(result_df)
