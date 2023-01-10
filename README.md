# A/B Testing Tool

Statistical significance is important because it allows researchers to hold a degree of confidence that their findings are real, reliable, and not events occurring due to chance or luck. This tool has been built keeping this in mind and aims at backing any sort of uplift observed with statistics.

What is an AB Test?

A/B testing (also known as split testing or bucket testing) is a method of comparing two campaigns against each other to determine which one performs better. A/B testing is essentially an experiment where statistical analysis is used on the performance of two campaigns to determine which campaign performs better for a given KPI goal and to back it with statistical confidence.

Hypothesis/Test Types:

A two-tailed test is appropriate when we believe either one of the strategies has overperformed or underperformed – could be both.

A one-tailed test is appropriate when we are to prove that either one of the strategies has either overperformed or underperformed. In this case, it could be only one of the two. The tool will automatically consider which one has a better KPI performance (CTR, VTR, CVR etc) and base the hypothesis that the campaign has performed well and undertake the calculations to back the lift.

Other Metrics:

A Z-score describes your deviation from the mean in units of standard deviation. It is not explicit as to whether you accept or reject your null hypothesis.

The power of hypothesis test is a measure of how effective the test is at identifying (say) a difference in populations if such a difference exists. It is the probability of rejecting the null hypothesis when it is false.

A p value is used in hypothesis testing to help you support or reject the null hypothesis. P values are expressed as decimals although it may be easier to understand what they are if you convert them to a percentage. For example, a p value of 0.0254 is 2.54%. This means there is a 2.54% chance your results could be random (i.e., happened by chance). That’s tiny. On the other hand, a large p-value of .9(90%) means your results have a 90% probability of being completely random and not due to anything in your experiment. Therefore, the smaller the p-value, the more important (“significant “) your results.


You can access the tool at - https://share.streamlit.io/allanabraham10/a-btest/main/streammain.py
