#  ProbDist Lab — Statistical Analysis Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458)
![NumPy](https://img.shields.io/badge/Numerical-NumPy-013243)
![SciPy](https://img.shields.io/badge/Statistics-SciPy-8CAAE6)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

> **Statistics Toolkit** is an interactive statistical analysis platform developed using **Python**, **Streamlit**, **Pandas**, **NumPy**, **SciPy**, and **Statsmodels**.
>
> The toolkit allows users to upload datasets, explore variables, generate visualizations, check statistical assumptions, fit probability distributions, perform hypothesis testing, run ANOVA, and understand statistical results through a simple dashboard interface.

---

##  Project Repository

GitHub Repository:

```text
https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
```

Replace this link with your final GitHub repository link.

---

##  Live Application

Access the deployed application here:

```text
Add your Streamlit deployment link here
```

Example:

```text
https://your-app-name.streamlit.app/
```

---

##  Project Objective

This project was developed as part of a statistical analysis toolkit assignment.

The main objective is to create a reusable and interactive application that helps users perform common statistical analyses without manually writing separate code for every test.

The toolkit is designed to help users:

* Upload and inspect datasets
* Understand dataset structure
* Generate descriptive statistics
* Create visualizations
* Check normality assumptions
* Demonstrate probability concepts
* Fit common probability distributions
* Perform hypothesis testing
* Conduct ANOVA
* Interpret statistical results

The application combines statistical methods with a simple user interface, making it useful for students, beginners, and anyone learning data analysis.

---

#  Key Features

---

## 1.  Dataset Upload and Management

Users can upload datasets directly into the application and begin analysis through the dashboard.

### Supported Format

* CSV (.csv)

### Dataset Overview

The application displays important dataset details such as:

* Number of rows
* Number of columns
* Numerical variables
* Categorical variables
* Missing values
* Dataset preview
* Column information

This helps users understand the structure and quality of the dataset before selecting statistical methods.

---

## 2.  Descriptive Statistics

The Descriptive Statistics module provides a summary of selected numerical variables.

### Available Measures

* Mean
* Median
* Variance
* Standard deviation
* Minimum value
* Maximum value
* Quartiles
* Interquartile range
* Skewness
* Kurtosis

This section helps users understand the central tendency, spread, and shape of the selected data.

---

## 3.  Data Visualization

The Visualization module provides graphical representations of the dataset.

### Available Visualizations

* Histogram
* Box plot
* Scatter plot
* Bar chart
* Line chart
* Distribution plot

These visualizations help users identify:

* Distribution patterns
* Data spread
* Possible outliers
* Relationships between variables
* Differences between groups

---

## 4.  Normality Testing

The Normality Testing module checks whether a selected numerical variable approximately follows a normal distribution.

### Purpose

Normality testing helps users decide whether parametric or nonparametric statistical methods are more suitable.

### Outputs

* Normality test result
* Test statistic
* P-value
* Statistical decision
* Result interpretation
* Supporting visualization

---

## 5.  Central Limit Theorem Demonstration

The Central Limit Theorem module demonstrates how sample means tend to form a normal-like distribution as sample size increases.

### Features

Users can select:

* Numerical variable
* Sample size
* Number of samples

### Outputs

* Original distribution
* Sampling distribution
* Summary statistics
* Interpretation of the sampling result

This section helps users understand one of the most important ideas in probability and statistics.

---

## 6.  Distribution Fitting

The Distribution Fitting module compares the selected numerical data with common probability distributions.

### Supported Distributions

* Normal Distribution
* Uniform Distribution
* Exponential Distribution

### Features

The module helps users:

* Fit probability distributions to data
* Compare distribution shapes
* Visualize fitted curves
* Review goodness-of-fit results
* Identify which distribution fits better

### Outputs

* Histogram of observed data
* Fitted distribution curves
* Distribution parameters
* Goodness-of-fit comparison
* Best-fit interpretation

This module helps users understand the underlying probability pattern of the selected variable.

---

#  Hypothesis Testing

---

## 7.  T-Tests

The toolkit includes common t-test procedures used for comparing means.

### One-Sample T-Test

Used to compare a sample mean with a known or hypothesized population mean.

### Independent Two-Sample T-Test

Used to compare the means of two independent groups.

### Paired Sample T-Test

Used to compare two related measurements, such as before-and-after values.

### Included Outputs

* Null hypothesis
* Alternative hypothesis
* Test statistic
* P-value
* Significance decision
* Result interpretation

---

## 8.  Z-Test

The Z-Test module is used when the population standard deviation is known or when the sample size is sufficiently large.

### Outputs

* Z statistic
* P-value
* Statistical decision
* Interpretation

---

## 9.  ANOVA

The ANOVA module is used to compare means across multiple groups.

### One-Way ANOVA

Used when comparing the means of three or more independent groups based on one factor.

### Two-Way ANOVA

Used when studying the effect of two factors and possible interaction effects.

### Outputs

* ANOVA table
* F-statistic
* Degrees of freedom
* P-value
* Statistical decision
* Interpretation

ANOVA helps users determine whether there are statistically significant differences between group means.

---

## 10.  Chi-Square Tests

The toolkit includes chi-square based analysis for categorical variables.

### Chi-Square Test of Independence

Used to check whether two categorical variables are associated.

### Chi-Square Goodness-of-Fit Test

Used to compare observed frequencies with expected frequencies.

### Outputs

* Contingency table
* Expected frequencies
* Chi-square statistic
* P-value
* Statistical decision
* Interpretation

---

## 11.  Nonparametric Tests

The toolkit includes nonparametric alternatives for cases where normality assumptions are not satisfied.

### Included Tests

#### Mann-Whitney U Test

Used to compare two independent groups when parametric assumptions are not met.

#### Wilcoxon Signed-Rank Test

Used for paired observations when the normality assumption is not met.

#### Kruskal-Wallis Test

Used to compare three or more independent groups when ANOVA assumptions are violated.

#### Friedman Test

Used for repeated measures or related groups when parametric assumptions are not suitable.

These tests make the toolkit useful even when the data does not follow a normal distribution.

---

#  Result Interpretation

Where applicable, the toolkit provides interpretation support for statistical results.

| Statistical Method  | Interpretation Focus                      |
| ------------------- | ----------------------------------------- |
| T-Test              | Difference between means                  |
| ANOVA               | Difference across multiple groups         |
| Chi-Square Test     | Association between categorical variables |
| Z-Test              | Difference from hypothesized value        |
| Nonparametric Tests | Difference based on ranks                 |

The result interpretation sections help users understand whether a result is statistically significant and what it means in simple terms.

---

#  Project Structure

```text
Statistics_Toolkit/
│
├── Home.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pages/
│   ├── 01_Data_Upload.py
│   ├── 02_Descriptive_Review.py
│   ├── 03_Visualization.py
│   ├── 04_Normality_Check.py
│   ├── 05_CLT_Demo.py
│   ├── 06_Distribution_Fit.py
│   ├── 07_Hypothesis_Tests.py
│   └── 08_ANOVA.py
│
└── src/
    ├── style.py
    ├── helpers.py
    └── stats_utils.py
```

Note: File names may differ slightly depending on the final project version.

---

#  Installation

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Statistics_Toolkit
```

## Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

## Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

## Step 5: Run the Application

If the main file is `Home.py`, run:

```bash
streamlit run Home.py
```

If the main file is `app.py`, run:

```bash
streamlit run app.py
```

After running the command, the application will open in the browser.

Usually, the local URL is:

```text
http://localhost:8501
```

---

#  How to Use the Toolkit

### Step 1

Open the application using Streamlit.

### Step 2

Upload a CSV dataset.

### Step 3

Review the dataset preview and column information.

### Step 4

Select a module from the sidebar.

### Step 5

Choose the required numerical or categorical variables.

### Step 6

Run the selected visualization, assumption check, distribution fit, or statistical test.

### Step 7

Review the output table, graph, statistical decision, and interpretation.

---

#  Technologies Used

| Technology  | Purpose                        |
| ----------- | ------------------------------ |
| Python      | Programming Language           |
| Streamlit   | Web Application Framework      |
| Pandas      | Data Manipulation              |
| NumPy       | Numerical Computing            |
| SciPy       | Statistical Analysis           |
| Statsmodels | Statistical Modeling and ANOVA |
| Matplotlib  | Data Visualization             |
| Plotly      | Interactive Charts             |

---

#  Assignment Requirement Coverage

| Requirement            | Implementation                               |
| ---------------------- | -------------------------------------------- |
| Data Import            | CSV Upload                                   |
| Dataset Exploration    | Dataset Preview and Column Details           |
| Missing Value Review   | Missing Value Summary                        |
| Descriptive Statistics | Summary Statistics Module                    |
| Data Visualization     | Histogram, Box Plot, Scatter Plot, Bar Chart |
| Probability Concepts   | Distribution Fitting and CLT Demonstration   |
| Normality Testing      | Normality Check Module                       |
| Hypothesis Testing     | T-Test, Z-Test, Chi-Square, ANOVA            |
| Nonparametric Methods  | Rank-Based Test Options                      |
| Interpretation         | Result Interpretation Sections               |
| Interactive Interface  | Streamlit Dashboard                          |
| Documentation          | README File                                  |

---

#  Future Improvements

Potential future enhancements include:

* PDF report generation
* Correlation analysis
* Regression analysis
* Confidence interval calculators
* Interactive report export
* Automated test recommendation
* More dataset cleaning tools
* Cloud deployment with public access

---

#  Author

**Gowtham Kumar Rajasekaran**

---

#  Final Note

Statistics Toolkit was developed as an educational statistical analysis platform.

The main goal of this project is not only to calculate statistical results, but also to help users understand the assumptions, decisions, and interpretations behind each method.

By combining descriptive statistics, visualization, assumption testing, distribution fitting, hypothesis testing, and ANOVA in one Streamlit dashboard, this toolkit provides a practical learning environment for statistical analysis.
