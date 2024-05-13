import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


data = pd.read_csv('C:\\Users\\roble\\OneDrive\\Documents\\machine learning tests\\creditscores - test1.csv')


exclude_cols = ['ID', 'Customer_ID', 'Month', 'Name', 'SSN', 'Occupation']
data = data.drop(columns=exclude_cols, errors='ignore')
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
categorical_cols = ['Type_of_Loan', 'Payment_Behaviour']
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_data = encoder.fit_transform(data[categorical_cols])
X_sparse = hstack([encoded_data, data[numeric_cols].values])
data['DebtToIncomeRatio'] = data['Total_EMI_per_month'] / data['Monthly_Inhand_Salary']
y = data['credit_score']
data_subset, _ = train_test_split(data, train_size=0.1, random_state=42)
numeric_cols_used = data_subset.select_dtypes(include=['float64', 'int64']).columns.difference(['credit_score'])


X_train_sparse, X_test_sparse, y_train, y_test = train_test_split(X_sparse, y, test_size=0.2, random_state=42)
regression_model = LinearRegression()
regression_model.fit(X_train_sparse, y_train)


def predict_user_credit_score(type_of_loan, payment_behaviour, total_emi_per_month, monthly_inhand_salary,
                              num_bank_accounts, num_credit_cards, interest_rate, num_of_loan, delay_from_due_date,
                              num_of_delayed_payment, changed_credit_limit, num_credit_inquiries, credit_mix,
                              outstanding_debt, credit_utilization_ratio, credit_history_age, payment_of_min_amount,
                              amount_invested_monthly):
    user_data = pd.DataFrame({
        'Type_of_Loan': [type_of_loan],
        'Payment_Behaviour': [payment_behaviour],
        'Total_EMI_per_month': [total_emi_per_month],
        'Monthly_Inhand_Salary': [monthly_inhand_salary],
        'Num_Bank_Accounts': [num_bank_accounts],
        'Num_Credit_Card': [num_credit_cards],
        'Interest_Rate': [interest_rate],
        'Num_of_Loan': [num_of_loan],
        'Delay_from_due_date': [delay_from_due_date],
        'Num_of_Delayed_Payment': [num_of_delayed_payment],
        'Changed_Credit_Limit': [changed_credit_limit],
        'Num_Credit_Inquiries': [num_credit_inquiries],
        'Credit_Mix': [credit_mix],
        'Outstanding_Debt': [outstanding_debt],
        'Credit_Utilization_Ratio': [credit_utilization_ratio],
        'Credit_History_Age': [credit_history_age],
        'Payment_of_Min_Amount': [payment_of_min_amount],
        'Amount_invested_monthly': [amount_invested_monthly],
        'DebtToIncomeRatio': [total_emi_per_month / monthly_inhand_salary]
    })

    user_data[numeric_cols_used] = user_data[numeric_cols_used].apply(pd.to_numeric, errors='coerce')
    X_user_numeric_sparse = csr_matrix(user_data[numeric_cols_used].values)
    encoded_user_data = encoder.transform(user_data[categorical_cols])
    X_user_sparse = hstack([encoded_user_data, X_user_numeric_sparse])
    user_credit_score = regression_model.predict(X_user_sparse)
    
    return user_credit_score[0]
