import streamlit as st
import scipy.stats
from scipy import stats
from scipy.stats import norm 
import numpy as np
import matplotlib.pyplot as plt

header = st.container()
credentials = st.container()
testing = st.container()

st.sidebar.header("What is an A/B Test?")
st.sidebar.write("A/B testing (also known as split testing or bucket testing) is a method of comparing two campaigns against each other to determine which one performs better. A/B testing is essentially an experiment where statistical analysis is used on the performance of two campaigns to determine which campaign performs better for a given KPI goal.")


st.sidebar.subheader("An overview of the test metrics")
with st.sidebar.expander("Hypothesis/Test Type"):
    #st.write("In statistical significance testing, a one-tailed test and a two-tailed test are alternative ways of computing the statistical significance of a parameter inferred from a data set, in terms of a test statistic. A two-tailed test is appropriate if the estimated value is greater or less than a certain range of values, for example, whether a test taker may score above or below a specific range of scores. This method is used for null hypothesis testing and if the estimated value exists in the critical areas, the alternative hypothesis is accepted over the null hypothesis. A one-tailed test is appropriate if the estimated value may depart from the reference value in only one direction, left or right, but not both. An example can be whether a machine produces more than one-percent defective products. In this situation, if the estimated value exists in one of the one-sided critical areas, depending on the direction of interest (greater than or less than), the alternative hypothesis is accepted over the null hypothesis. Alternative names are one-sided and two-sided tests; the terminology 'tail' is used because the extreme portions of distributions, where observations lead to rejection of the null hypothesis, are small and often 'tail off' toward zero.")
    st.write("A two-tailed test is appropriate if the estimated value is greater or less than a certain range of values, for example, whether a test taker may score above or below a specific range of scores. This method is used for null hypothesis testing and if the estimated value exists in the critical areas, the alternative hypothesis is accepted over the null hypothesis. A one-tailed test is appropriate if the estimated value may depart from the reference value in only one direction, left or right, but not both. An example can be whether a machine produces more than one-percent defective products.")
    
with st.sidebar.expander("Confidence"):
    st.write("Confidence intervals gives us a range of possible values and an estimate of the precision for our parameter value. Esentially, we are saying if we were to sample many many times, and calculate confidence intervals for a certain paremeter like a mean or regression coefficient, we can then expect about 95 out of 100 of those intervals to capture the true population parameter.")

with st.sidebar.expander("z score"):
    st.write("A Z-score describes your deviation from the mean in units of standard deviation. It is not explicit as to whether you accept or reject your null hypothesis.")    

with st.sidebar.expander("Power"):
    st.write("The power of hypothesis test is a measure of how effective the test is at identifying (say) a difference in populations if such a difference exists. It is the probability of rejecting the null hypothesis when it is false.")
    
with st.sidebar.expander("p value"):
    st.write("A p value is used in hypothesis testing to help you support or reject the null hypothesis. P values are expressed as decimals although it may be easier to understand what they are if you convert them to a percentage. For example, a p value of 0.0254 is 2.54%. This means there is a 2.54% chance your results could be random (i.e. happened by chance). That’s pretty tiny. On the other hand, a large p-value of .9(90%) means your results have a 90% probability of being completely random and not due to anything in your experiment. Therefore, the smaller the p-value, the more important (“significant“) your results.")


with header:
    st.title("A/B Test Calculator")
    
with credentials:
    with st.form("Form1"):
        cola, colb = st.columns(2)
        name = cola.text_input("Enter your Name","my name")
        team = colb.selectbox("Select your role",options=["my role","Analyst","Account Manager","Trader","CS"])
        submitted1 = st.form_submit_button('Submit')
        if (len(name)<3 or name=="my name" or any(map(str.isdigit, name)) or team=="my role"):
            st.warning("Please enter valid user info")
            st.stop()
    
with testing:
    col1, col2, col3 = st.columns(3)
    imp_a = col1.text_input("Enter Delivery for Group A",'379990')
    imp_b = col1.text_input("Enter Delivery for Group B",'652515')
    conv_a = col2.text_input('Enter KPI Results for Group A','102')
    conv_b = col2.text_input('Enter KPI Results for Group B','228')
    
    hypothesis = col3.selectbox("Choose the Test Type",options=["One Tailed","Two Tailed"])

    confidence = col3.radio("Select the Confidence",options=["90%","95%","99%"])
    
    if(col2.button("Submit")==False):
        st.write("Submit your Input")
        st.stop()
    
    
    try:
        int(imp_a)
        int(imp_b)
        int(conv_a)
        int(conv_b)
    
    except:
        st.error("Please enter valid data")
        st.stop()

    conv_rate_a = int(conv_a)/int(imp_a)
    conv_rate_b = int(conv_b)/int(imp_b)
    relative_uplift = (conv_rate_b - conv_rate_a)/conv_rate_a
    se_a = pow(conv_rate_a*(1-conv_rate_a)/int(imp_a),0.5)
    se_b = pow(conv_rate_b*(1-conv_rate_b)/int(imp_b),0.5)

    if(conv_rate_a > conv_rate_b):
        st.error("Insignificant Results! The CVR of the Test campaign is lower.")
        st.stop()

    se_diff = pow((pow(se_a,2)+pow(se_b,2)),0.5)
    z_score = (conv_rate_b - conv_rate_a)/se_diff

    p_value = 0
    if(hypothesis == "One Tailed"):
        p_value = scipy.stats.norm.sf(abs(z_score))
    elif(hypothesis == "Two Tailed"):
        p_value = scipy.stats.norm.sf(abs(z_score))*2

    alpha = 0
    if(confidence == "90%"):
        alpha = 0.1
    elif(confidence == "95%"):
        alpha = 0.05
    elif(confidence == "99%"):
        alpha = 0.01

    if(p_value<alpha):
        st.balloons()
        st.success("Your results are statistically significant! You can be {} sure that the uplift of {}% is a consequence of the changes you made and not a result of random chance.".format(confidence,round(relative_uplift*100,2)))
    else:
        st.warning("Statistically insignificant results! The uplift of {}% need not be a consequence of the changes you made and could be a result of random chance.".format(round(relative_uplift*100,2)))

    #Power of the Test
    if(hypothesis == "One Tailed"):
        z_crit = stats.norm.ppf(1-alpha)
        X_c = (z_crit*se_a)+conv_rate_a
        power = 1-norm(conv_rate_b, se_b).cdf(np.absolute(X_c))
    elif(hypothesis == "Two Tailed"):
        z_crit = stats.norm.ppf(1-alpha/2)
        X_c = (z_crit*se_a)+conv_rate_a
        power = 1-norm(conv_rate_b, se_b).cdf(np.absolute(X_c))

###############################################################################################################################################################

    #Graph Function
    class A_One:
      @staticmethod
      def plot(mean, std, lower_bound=None, upper_bound=None, resolution=None,
        title=None, x_label=None, y_label=None, legend_label=None, legend_location=(1.05,0.5)):

        lower_bound = ( mean - 4*std ) if lower_bound is None else lower_bound
        upper_bound = ( mean + 4*std ) if upper_bound is None else upper_bound
        resolution  = 100

        title        = title        or "A/B Testing"
        #x_label      = x_label      or "x"
        #y_label      = y_label      or "N(x|μ,σ)"
        #legend_label = legend_label or "μA={}, σA={}".format(mean, std)
        legend_label = legend_label or "Control Group"

        X = np.linspace(lower_bound, upper_bound, resolution)
        dist_X = A_One._distribution(X, mean, std)

        plt.title(title)

        plt.plot(X, dist_X, label=legend_label)
        #plt.axvline(mean, color = 'y',label = 'Conversion Rate A = {}%'.format(conv_rate_a*100))
        plt.axvline(mean, color = 'y')
        plt.axvline(X_c, color = 'r', label = 'Confidence: {}%'.format(100-alpha*100)) 

        #plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc=legend_location)

        return plt

      @staticmethod
      def _distribution(X, mean, std):
        return 1./(np.sqrt(2*np.pi)*std)*np.exp(-0.5 * (1./std*(X - mean))**2)


    class A_Two:
      @staticmethod
      def plot(mean, std, lower_bound=None, upper_bound=None, resolution=None,
        title=None, x_label=None, y_label=None, legend_label=None, legend_location=(1.05,0.5)):

        lower_bound = ( mean - 4*std ) if lower_bound is None else lower_bound
        upper_bound = ( mean + 4*std ) if upper_bound is None else upper_bound
        resolution  = 100

        title        = title        or "A/B Testing"
        #x_label      = x_label      or "x"
        #y_label      = y_label      or "N(x|μ,σ)"
        #legend_label = legend_label or "μA={}, σA={}".format(mean, std)
        legend_label = legend_label or "Control Group"

        X = np.linspace(lower_bound, upper_bound, resolution)
        dist_X = A_Two._distribution(X, mean, std)

        plt.title(title)

        plt.plot(X, dist_X, label=legend_label)
        #plt.axvline(mean, color = 'y', label = 'Conversion Rate A = {}%'.format(conv_rate_a*100))
        plt.axvline(mean, color = 'y')
        plt.axvline(X_c, color = 'r', label = 'Confidence: {}%'.format(100-alpha*100))
        plt.axvline(2*mean-X_c, color = 'r') 

        #plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc=legend_location)

        return plt

      @staticmethod
      def _distribution(X, mean, std):
        return 1./(np.sqrt(2*np.pi)*std)*np.exp(-0.5 * (1./std*(X - mean))**2)

    class B:
      @staticmethod
      def plot(mean, std, lower_bound=None, upper_bound=None, resolution=None,
        title=None, x_label=None, y_label=None, legend_label=None, legend_location=(1.05,0.5)):

        lower_bound = ( mean - 4*std ) if lower_bound is None else lower_bound
        upper_bound = ( mean + 4*std ) if upper_bound is None else upper_bound
        resolution  = 100

        title        = title        or "A/B Testing"
        #x_label      = x_label      or "x"
        #y_label      = y_label      or "N(x|μ,σ)"
        #legend_label = legend_label or "μB={}, σB={}".format(mean, std)
        legend_label = legend_label or "Test Group"

        X = np.linspace(lower_bound, upper_bound, resolution)
        dist_X = B._distribution(X, mean, std)

        plt.title(title)

        plt.plot(X, dist_X, label=legend_label)
        #plt.axvline(mean, color = 'y', label = 'Conversion Rate B = {}%'.format(conv_rate_b*100))
        plt.axvline(mean, color = 'y')

        #plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc=legend_location)

        return plt

      @staticmethod
      def _distribution(X, mean, std):
        return 1./(np.sqrt(2*np.pi)*std)*np.exp(-0.5 * (1./std*(X - mean))**2)

###############################################################################################################################################################

    if(hypothesis == "One Tailed"):
        plot = A_One.plot(conv_rate_a, se_a)
    elif(hypothesis == "Two Tailed"):
        plot = A_Two.plot(conv_rate_a, se_a)
    plot = B.plot(conv_rate_b, se_b)

    st.pyplot(plot)

    col11, col12, col13 = st.columns(3)

    # col11.write("Conversion rate of Control Group: {}%".format(round(conv_rate_a*100,2)))
    # col12.write("Conversion rate of Test Group: {}%".format(round(conv_rate_b*100,2)))
    # col11.write("The Power of the Test is : {}%".format(round(power*100,2)))
    # col12.write("The p value of the Test is : {}".format(round(p_value,4)))
    # col13.write("The Significane Level (alpha) of the Test is : {}".format(round(alpha,2)))
    # col13.write("Uplift observed: {}%".format(round(relative_uplift*100,2)))

    col11.write("Conversion Rate Control Group")
    col11.write(str(round(conv_rate_a*100,3))+"%")
    col12.write("Conversion Rate Test Group")
    col12.write(str(round(conv_rate_b*100,3))+"%")
    col11.write("Power of the Test")
    col11.write(str(round(power*100,2))+"%")
    col12.write("p value of the Test")
    col12.write(str(round(p_value,4)))
    col13.write("Relative Uplift Observed")
    col13.write(str(round(relative_uplift*100,2))+"%")
    col13.write("Z score of the test")
    col13.write(str(round(z_score,4)))
