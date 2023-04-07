detail_markdown_text = r'''# Team Fitbit Challenge 
March 2023

## Proposed Scoring Metric

The data we collected daily per person is: 
- Active Minutes
- Number of Steps

Ideally, we could weight each of these data axes 'equally' -- that is, we could treat each of equal importance in determining the overall score per person (and per team.) Said another way, we'd like for the relative importance of each quantity to be equal in establishing a component of the overall score. 

One issue is that the units of each are different. For example, people are much more likely to take many more steps per day than they are to have active minutes. We could seek to normalize each of these value along a consistent axis, to make comparisons consistent. That is, we could make each quantity 'dimensionless' by dividing it by the 'characteristic length scale' of the quantity. (At least, that's what a theoretical physics nerd would likely do.)

But the main question would be -- how do we choose the characteristic length scale? I propose using the built-in daily target from the Fitbit app for each. That is, the default goal per day is 10,000 steps and 22 active minutes. 

If we choose these as the characteristic length scales, we can then divide each person's daily value by its corresponding length to get a normalized score. Then we could sum the score per team to get the total score per day.

So, the formula for the score per day for player $p$ would look like:

$$ {Score} \equiv \theta_p = \frac{\alpha_p}{22} + \frac{\sigma_p}{10,000}$$

Where $\alpha_p$ is the number of active minutes for player $p$ on that day, and $\sigma_p$ is the number of steps for player $p$ on that day. Another way of thinking of this could be that each additional active minute is effectively worth the same as an additional $\frac{10,000}{22}\approx 450$ steps.

As others have mentioned, we have special cases where some people were sick or injured or had a dead Fitbit on certain days, so we could just not include those data points in the calculation of the daily average per team.

$$ Team Score Per Day = \frac{\sum_{p}{\theta_p}}{N_t} $$

Here, $N_t$ is the number of active members of the team on the day, $\theta_i$ is the score for player $p$. A team member is considered 'active' if he or she contributes towards either steps or active minutes (or both) for that day.

Then, the total score per team for the challenge would be the sum of the daily scores.

You could also multiply the final score by a larger number like 500 and take the integer part, to avoid dealing with fractions and decimals. By using a value of 500, if you score the goal value of 10,000 steps for the day, and you score the goal of 22 minutes for the day, you will have an individual player score of 1000 for the day. '''
