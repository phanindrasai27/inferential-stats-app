import streamlit as st
import pandas as pd
from scipy.stats import ttest_ind, f_oneway, chi2_contingency

# Load CSV data into a pandas DataFrame
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to perform t-test
def perform_t_test(group1_data, group2_data):
    t_statistic, p_value = ttest_ind(group1_data, group2_data)
    return t_statistic, p_value

# Function to perform ANOVA
def perform_anova(groups_data):
    f_statistic, p_value = f_oneway(*groups_data)
    return f_statistic, p_value

# Function to perform chi-square test
def perform_chi_square(data):
    chi2_statistic, p_value, dof, expected = chi2_contingency(data)
    return chi2_statistic, p_value

# Main Streamlit app code
st.title("Inferential Statistics Comparison")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)

    st.write("Loaded CSV Data:")
    st.write(data)

    selected_test = st.selectbox("Select a statistical test", ["Independent Samples t-test", "One-way ANOVA", "Chi-Square Test"])

    if selected_test == "Independent Samples t-test":
        st.write("Select two columns for comparison:")
        selected_columns = st.multiselect("Select columns for comparison", data.columns)

        if len(selected_columns) == 2:
            group1_data = data[selected_columns[0]]
            group2_data = data[selected_columns[1]]

            t_statistic, p_value = perform_t_test(group1_data, group2_data)

            st.write("T-Test Results:")
            st.write("T-Statistic:", t_statistic)
            st.write("P-Value:", p_value)

            if 0.01 <= p_value <= 0.05:
                st.write("P-value suggests a moderate level of significance.")
                st.write("Mean of", selected_columns[0], ":", group1_data.mean())
                st.write("Mean of", selected_columns[1], ":", group2_data.mean())
                st.write("Conclusion: There might be a significant difference between the groups.")
            elif p_value < 0.01:
                st.write("P-value suggests a strong level of significance.")
                st.write("Mean of", selected_columns[0], ":", group1_data.mean())
                st.write("Mean of", selected_columns[1], ":", group2_data.mean())
                st.write("Conclusion: There is a significant difference between the groups.")
            else:
                st.write("P-value suggests no significant difference between the groups.")

    # Similar sections for ANOVA and Chi-Square tests

    elif selected_test == "One-way ANOVA":
        st.write("Select a column for grouping:")
        group_column = st.selectbox("Select a column for grouping", data.columns)

        selected_columns = st.multiselect("Select columns for comparison", data.columns)

        if group_column and selected_columns:
            groups_data = [group_data for _, group_data in data.groupby(group_column)[selected_columns[0]]]

            f_statistic, p_value = perform_anova(groups_data)

            st.write("ANOVA Results:")
            st.write("F-Statistic:", f_statistic)
            st.write("P-Value:", p_value)

            if p_value < 0.05:
                st.write("P-value suggests a significant difference between groups.")
                for i, column in enumerate(selected_columns):
                    st.write("Mean of", column, "for group", data[group_column].unique()[i], ":", data[column].mean())
                st.write("Conclusion: There is a significant difference between at least one pair of groups.")
            else:
                st.write("P-value suggests no significant difference between groups.")

    elif selected_test == "Chi-Square Test":
        st.write("Select two categorical columns for comparison:")
        selected_columns = st.multiselect("Select columns for comparison", data.columns)

        if len(selected_columns) == 2:
            crosstab_data = pd.crosstab(data[selected_columns[0]], data[selected_columns[1]])

            chi2_statistic, p_value = perform_chi_square(crosstab_data)

            st.write("Chi-Square Test Results:")
            st.write("Chi-Square Statistic:", chi2_statistic)
            st.write("P-Value:", p_value)

            if p_value < 0.05:
                st.write("P-value suggests a significant association between the variables.")
                st.write("Conclusion: There is evidence of a relationship between the categorical variables.")
            else:
                st.write("P-value suggests no significant association between the variables.")
