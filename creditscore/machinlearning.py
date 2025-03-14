import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, balanced_accuracy_score
import toad
import math
import matplotlib.pyplot as plt
from sklearn.metrics import recall_score, precision_score, f1_score

def data_split(data, start, end, date_col):
    return data[(data[date_col] >= start) & (data[date_col] < end)].reset_index(drop=True)


def calculate_evaluation_metrics(actual_labels, predicted_probabilities, threshold=0.5):
    """Calculates various evaluation metrics for binary classification."""

    binary_predictions = (predicted_probabilities > threshold).astype(int)
    accuracy = accuracy_score(actual_labels, binary_predictions)
    recall = recall_score(actual_labels, binary_predictions)
    precision = precision_score(actual_labels, binary_predictions)
    f1 = f1_score(actual_labels, binary_predictions)
    balanced_accuracy = balanced_accuracy_score(actual_labels, binary_predictions)

    return precision, recall, f1, accuracy, balanced_accuracy

def assign_credit_level(data, score_column, level_column, level_boundaries):
    """Assigns credit levels based on credit scores and defined boundaries."""

    credit_levels = []
    for score in data[score_column]:
        for i, boundary in enumerate(level_boundaries):
            if score <= boundary:
                credit_levels.append(i)
                break

    data[level_column] = credit_levels
    return data

def calculate_loss_coverage(data, target_level_column):
    """Calculates loss and coverage for different credit levels."""

    for level in range(8, 0, -1):
        level_subset = data[data[target_level_column] >= level]
        loss = level_subset['label'].value_counts()[1] / len(level_subset)
        coverage = level_subset['label'].value_counts()[0] / data[data.label == 0].shape[0]
        print(f"Level {level}: Loss is {loss:.4f}; Coverage is {coverage:.4f}")

#load Data
data = pd.read_csv('C:\\Users\\roble\\OneDrive\\Documents\\machine learning tests\\UCI_Credit_Card.csv')
# the label will be used as my tagert to see how likey it it teh user will payback next month
data['label'] = data['default.payment.next.month']
data = data.drop(columns=['default.payment.next.month'])

# i dont need these
exclude_list = ['ID', 'label']

# through jupyter notbook tetsing i know th there is 3000 collums so i feel like that this is a fair split
train = data_split(data, start=0, end=22500, date_col='ID')
test = data_split(data, start=22500, end=172792, date_col='ID')

# Selecting features from the training dataset using Toad's selection tool, filtering out features based on my criteria: retain those with less than 50% missing values ('empty'), an Information Value (IV) above 0.07 for relevance, and a pairwise correlation below 0.9 to reduce multicollinearity.
train_selected = toad.selection.select(frame=train, target=train['label'], empty=0.5, iv=0.07, corr=0.9, exclude=exclude_list)


# i Initialised and fit a Toad Combiner to discretise continuous variables using the Chi-squared method with a minimum sample size of 5%.
combiner = toad.transform.Combiner()
combiner.fit(X=train_selected, y=train_selected['label'], method='chi', min_samples=0.05, exclude=exclude_list)
# Excluded specified columns from transformation. The fitted combiner is then serialized and saved to a file for later use.
pickle.dump(combiner, open('CreditScore_save1_combiner.pkl', 'wb'))

# Appling the trained Toad Combiner to the training dataset to transform continuous variables into categorical bins based on the rules above
train_selected_bin = combiner.transform(train_selected)
# Then apply the same transformation to the test dataset using only the columns selected during the training phase.
test_bin = combiner.transform(test[train_selected_bin.columns])

t = toad.transform.WOETransformer()
train_woe = t.fit_transform(X=train_selected_bin, y=train_selected_bin['label'], exclude=exclude_list)
test_woe = t.transform(test_bin)


final_data_woe = pd.concat([train_woe, test_woe])


pickle.dump(t, open('CreditScore_save2_woe_transform.pkl', 'wb'))


features_use = [feat for feat in final_data_woe.columns if feat not in exclude_list]


df_iv = toad.quality(final_data_woe[features_use + ['label']], 'label', iv_only=True)



lr = LogisticRegression(class_weight='balanced')
lr.fit(train_woe[features_use], train_woe['label'])
probs_lr = lr.predict_proba(test_woe[features_use])[:, 1]


precision, recall, f1, accuracy, balanced_accuracy = calculate_evaluation_metrics(test_woe['label'], probs_lr)
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')
print(f'Accuracy: {accuracy:.4f}')
print(f'Balanced Accuracy: {balanced_accuracy:.4f}')

# ScoreCard model
card = toad.ScoreCard(
    combiner=combiner,
    transer=t,
    class_weight='balanced',
    C=0.1,
    base_score=999,
    base_odds=35,
    pdo=80,
    rate=2
)

card.fit(train_woe[features_use], train_woe['label'])
pickle.dump(card, open('CreditScore_save5_ScoreCard.pkl', 'wb'))


keys = list(card.export().keys())
score_card_df = pd.DataFrame()

score_card_dfs = []

for n in keys:
    temp = pd.DataFrame.from_dict(card.export()[n], orient='index').reset_index()
    temp.columns = ['binning', 'score']
    temp['variable'] = n
    temp = temp[['variable', 'binning', 'score']]
    score_card_dfs.append(temp)

score_card_df = pd.concat(score_card_dfs, ignore_index=True)
score_card_df.to_csv('CreditScore_save6_score_card_df.csv', index=False)

if 'CreditScore' in final_data_woe.columns:
    w = 40
    n = math.ceil((final_data_woe['CreditScore'].max() - final_data_woe['CreditScore'].min()) / w)

    plt.hist(final_data_woe[final_data_woe.label == 1].CreditScore, alpha=0.5, label='Fraud', bins=n)
    plt.hist(final_data_woe[final_data_woe.label == 0].CreditScore, alpha=0.5, label='Not Fraud', bins=n)
    plt.legend(loc='upper left')
    plt.title('Credit Score Distribution: Test Set', size=15)
    plt.show()

  
    assign_credit_level(final_data_woe, score_column='CreditScore', level_column='CreditScore_level',
                        level_boundaries=[250, 300, 400, 500, 580, 630, 690, 730, 1000])

    calculate_loss_coverage(final_data_woe, target_level_column='CreditScore_level')

   
    final_data_woe.to_csv('CreditScore_save7_whole_data.csv', index=False)

    
    def get_user_input():
        user_data = {}
        user_data['ID'] = float(input("Enter ID: "))

        user_df = pd.DataFrame([user_data])
        return user_df

    def predict_credit_score(user_df, card_model):
        card = pickle.load(open(card_model, 'rb'))
        user_df['CreditScore'] = card.predict(user_df)
        user_df['CreditScore_level'] = card.predict_proba(user_df)[:, 1]
        return user_df


    user_input = get_user_input()
    credit_score_result = predict_credit_score(user_input, 'CreditScore_save5_ScoreCard.pkl')

    print(credit_score_result[['ID', 'CreditScore', 'CreditScore_level']])
else:
    print("Column 'CreditScore' not found in the DataFrame.")


def get_user_input():
    # Collect all the user inputs
    user_data = {}
    user_data['ID'] = float(input("Enter ID: "))
    user_data['LIMIT_BAL'] = float(input("Enter LIMIT_BAL: "))
    user_data['SEX'] = float(input("Enter SEX (1 for male, 2 for female): "))
    user_data['EDUCATION'] = float(input("Enter EDUCATION: "))
    user_data['MARRIAGE'] = float(input("Enter MARRIAGE: "))
    user_data['AGE'] = float(input("Enter AGE: "))
    user_data['PAY_0'] = float(input("Enter PAY_0: "))
    user_data['PAY_2'] = float(input("Enter PAY_2: "))
    user_data['PAY_3'] = float(input("Enter PAY_3: "))
    user_data['PAY_4'] = float(input("Enter PAY_4: "))
    user_data['PAY_5'] = float(input("Enter PAY_5: "))
    user_data['PAY_6'] = float(input("Enter PAY_6: "))
    user_data['BILL_AMT1'] = float(input("Enter BILL_AMT1: "))
    user_data['BILL_AMT2'] = float(input("Enter BILL_AMT2: "))
    user_data['BILL_AMT3'] = float(input("Enter BILL_AMT3: "))
    user_data['BILL_AMT4'] = float(input("Enter BILL_AMT4: "))
    user_data['BILL_AMT5'] = float(input("Enter BILL_AMT5: "))
    user_data['BILL_AMT6'] = float(input("Enter BILL_AMT6: "))
    user_data['PAY_AMT1'] = float(input("Enter PAY_AMT1: "))
    user_data['PAY_AMT2'] = float(input("Enter PAY_AMT2: "))
    user_data['PAY_AMT3'] = float(input("Enter PAY_AMT3: "))
    user_data['PAY_AMT4'] = float(input("Enter PAY_AMT4: "))
    user_data['PAY_AMT5'] = float(input("Enter PAY_AMT5: "))
    user_data['PAY_AMT6'] = float(input("Enter PAY_AMT6: "))

    # Creating a DataFrame from all user inputs
    user_df = pd.DataFrame([user_data])

    return user_df

def predict_credit_score(user_df, card_model):
    # Load the saved ScoreCard model
    card = pickle.load(open(card_model, 'rb'))

    # Predict credit score using the model
    probabilities = card.predict_proba(user_df)

    # just a few debug statments
    print("Dimensions of probabilities:", probabilities.shape if probabilities is not None else None)
    print("user_df columns:", user_df.columns)

    # Check if the probabilities are available and non-empty
    if probabilities is not None and len(probabilities) > 0:
        
        user_df['CreditScore'] = card.predict(user_df)
        user_df['CreditScore_level'] = probabilities[0, 1]
    else:
        
        user_df['CreditScore'] = None
        user_df['CreditScore_level'] = None

    return user_df



