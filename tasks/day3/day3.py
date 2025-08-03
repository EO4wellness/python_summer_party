# Outline the logic, then write the Python code, to solve this scenario.  
# This is question one of a three-question series which follow these same assumptions.
# 
# Context: You are a data analyst working with the Disney Parks revenue team to understand nuanced guest spending 
# patterns across different park experiences. The team wants to develop a comprehensive view of visitor purchasing 
# behaviors. Your goal is to uncover meaningful insights that can drive personalized marketing strategies.
# 
# Question 1: What is the average spending per guest per visit for each park experience type during July 2024?
# Ensure that park experience types with no recorded transactions are shown with an average spending of 0.0. 
# This analysis helps establish baseline spending differences essential for later segmentation.
# Assumptions: Tables fct_guest_spending(guest_id, visit_date, park_experience_type, amount_spent)
# Note: pandas and numpy are already imported as pd and np in the workspace environment. 
# The following tables are loaded as pandas DataFrames with the same names: fct_guest_spending
# Please print your final result or dataframe
#
# Logic Breakdown
# Goal
# For each park experience type, calculate the average spending per guest per visit for July 2024, 
# including 0.0 for types with no spending data.
# Step-by-Step Logic
# - Filter for July 2024 visits
# Extract rows where visit_date falls within July 2024.
# - Aggregate guest visit spending
# Group by guest_id, visit_date, and park_experience_type to get total spending per guest per visit.
# - Calculate average per experience type
# Group the above result by park_experience_type to get the average of those visit totals.
# - Ensure 0.0 for missing experience types
# Create a complete list of all possible park_experience_type values, and merge so any missing types show up with 0.0
#
# # Step 1: Filter to July 2024
july_data = fct_guest_spending[
    (fct_guest_spending['visit_date'] >= '2024-07-01') &
    (fct_guest_spending['visit_date'] <= '2024-07-31')
]

# Step 2: Total per guest per visit per experience
visit_totals = july_data.groupby(
    ['guest_id', 'visit_date', 'park_experience_type'],
    as_index=False
)['amount_spent'].sum()

# Step 3: Average spending per experience type
avg_spending = visit_totals.groupby(
    'park_experience_type',
    as_index=False
)['amount_spent'].mean()

# Rename for clarity
avg_spending.rename(columns={'amount_spent': 'avg_spending_per_guest_visit'}, inplace=True)

# Step 4: Fill in missing experience types with 0.0
all_types = fct_guest_spending['park_experience_type'].drop_duplicates()
all_types_df = pd.DataFrame({'park_experience_type': all_types})

# Left join to include all experience types
final_result = all_types_df.merge(avg_spending, on='park_experience_type', how='left')

# Fill missing values with 0.0
final_result['avg_spending_per_guest_visit'] = final_result['avg_spending_per_guest_visit'].fillna(0.0)

# Display final DataFrame
print(final_result)

# Question 2: For guests who visited our parks more than once in August 2024, what is the difference in spending 
# between their first and their last visit? This investigation, using sequential analysis, will reveal any shifts 
# in guest spending behavior over multiple visits.
# 
# Goal
# For guests who visited more than once in August 2024, compute the difference in total spending between their
# first visit and last visit.
#
# Step-by-Step Logic
# - Filter for August 2024 visits
# Select rows where visit_date falls in August 2024.
# - Aggregate guest spending per visit date
# Sum amount_spent by guest_id and visit_date.
# - Identify first and last visit per guest
# For guests with more than one visit, determine the earliest and latest visit dates.
# - Extract spending on first and last visits
#Retrieve the amount spent on both visit dates for each guest.
# - Calculate spending difference
# Subtract first visit spending from last visit spending
# - Ensure results are presented with guest_id, first visit spending, last visit spending, and the difference.
#
# Step 1: Filter for August 2024
aug_data = fct_guest_spending[
    (fct_guest_spending['visit_date'] >= '2024-08-01') &
    (fct_guest_spending['visit_date'] <= '2024-08-31')
]

# Step 2: Total spend per guest per date
guest_visit_spend = aug_data.groupby(
    ['guest_id', 'visit_date'],
    as_index=False
)['amount_spent'].sum()

# Step 3: First and last visit dates per guest (with >1 visit)
visit_counts = guest_visit_spend.groupby('guest_id')['visit_date'].count()
multi_visitors = visit_counts[visit_counts > 1].index

# Filter to multi-visit guests only
multi_visits_df = guest_visit_spend[guest_visit_spend['guest_id'].isin(multi_visitors)]

# Step 4: Identify first and last visits
first_visits = multi_visits_df.loc[multi_visits_df.groupby('guest_id')['visit_date'].idxmin()]
last_visits  = multi_visits_df.loc[multi_visits_df.groupby('guest_id')['visit_date'].idxmax()]

# Merge to get both visits side by side
spending_diff = pd.merge(
    first_visits,
    last_visits,
    on='guest_id',
    suffixes=('_first', '_last')
)

# Step 5: Calculate spending difference
spending_diff['spending_difference'] = (
    spending_diff['amount_spent_last'] - spending_diff['amount_spent_first']
)

# Display result
print(spending_diff[['guest_id', 'amount_spent_first', 'amount_spent_last', 'spending_difference']])

# Question 3: In September 2024, how can guests be categorized into distinct spending segments such as Low, 
# Medium, and High based on their total spending? Use the following thresholds for categorization: 
# -Low: Includes values from $0 up to, but not including, $50. 
# -Medium: Includes values from $50 up to, but not including, $100. 
# -High: Includes values from $100 and above. 
# Exclude guests who did not make any purchases in the period.
#
# Goal
# Classify guests based on total September 2024 spending using the thresholds:
# - Low: $0 ≤ spend < $50
# - Medium: $50 ≤ spend < $100
# - High: $100 and above
# Exclude those with no spending (i.e., total = $0).
# Step-by-Step Logic
# - Filter for visits in September 2024
# Select rows where visit_date falls in September 2024.
# - Aggregate total spending per guest
# Group by guest_id to get the sum of amount_spent.
# - Exclude non-spending guests
# Remove any guests whose total spending is 0.
# - Apply categorical labels
# Use pd.cut() to bucket spending into Low, Medium, High.
#
# Step 1: Filter for September 2024
sep_data = fct_guest_spending[
    (fct_guest_spending['visit_date'] >= '2024-09-01') &
    (fct_guest_spending['visit_date'] <= '2024-09-30')
]

# Step 2: Total spending per guest
guest_total_spend = sep_data.groupby('guest_id', as_index=False)['amount_spent'].sum()

# Step 3: Exclude guests with $0 total spend
guest_total_spend = guest_total_spend[guest_total_spend['amount_spent'] > 0]

# Step 4: Categorize spending levels
bins = [0, 50, 100, np.inf]
labels = ['Low', 'Medium', 'High']
guest_total_spend['spending_category'] = pd.cut(
    guest_total_spend['amount_spent'],
    bins=bins,
    labels=labels,
    right=False  # Makes upper bound exclusive
)

# Display result
print(guest_total_spend[['guest_id', 'amount_spent', 'spending_category']])







